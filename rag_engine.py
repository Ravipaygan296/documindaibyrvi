"""
RAG Engine — Core Document Intelligence Logic
Handles: PDF parsing → Chunking → Embedding → FAISS indexing → Retrieval → LLM generation
"""

import os
import io
import numpy as np
from typing import List, Dict, Any
import PyPDF2
from sentence_transformers import SentenceTransformer
import faiss


class RAGEngine:
    """
    End-to-end RAG pipeline:
    1. PDF parsing  →  extract text per page
    2. Chunking     →  split into overlapping text chunks
    3. Embedding    →  encode chunks with SentenceTransformers
    4. Indexing     →  store in FAISS for fast similarity search
    5. Retrieval    →  find top-k relevant chunks for a query
    6. Generation   →  send context + query to LLM for final answer
    """

    def __init__(
        self,
        api_key: str,
        provider: str = "groq",
        model_name: str = "llama3-8b-8192",
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        top_k: int = 3,
        embedding_model: str = "all-MiniLM-L6-v2"
    ):
        self.api_key = api_key
        self.provider = provider
        self.model_name = model_name
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.top_k = top_k

        # Load embedding model (runs locally, no API needed)
        print("Loading embedding model...")
        self.embedder = SentenceTransformer(embedding_model)

        # Will be populated after processing docs
        self.index = None
        self.chunks = []          # list of {"content": str, "file": str, "page": int}
        self.doc_names = []

    # ─── Step 1: PDF Parsing ─────────────────────────────────────────────────
    def parse_pdf(self, file_bytes: bytes, filename: str) -> List[Dict]:
        """Extract text from each page of a PDF."""
        pages = []
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            text = text.strip()
            if text:
                pages.append({
                    "content": text,
                    "file": filename,
                    "page": page_num + 1
                })
        return pages

    # ─── Step 2: Chunking ────────────────────────────────────────────────────
    def chunk_text(self, text: str, file: str, page: int) -> List[Dict]:
        """Split text into overlapping chunks for better retrieval."""
        words = text.split()
        chunks = []
        start = 0
        while start < len(words):
            end = min(start + self.chunk_size, len(words))
            chunk_text = " ".join(words[start:end])
            if len(chunk_text.strip()) > 50:  # skip tiny chunks
                chunks.append({
                    "content": chunk_text,
                    "file": file,
                    "page": page
                })
            start += self.chunk_size - self.chunk_overlap
        return chunks

    # ─── Step 3 & 4: Embedding + FAISS Indexing ──────────────────────────────
    def build_index(self, chunks: List[Dict]):
        """Embed all chunks and build a FAISS index for fast retrieval."""
        texts = [c["content"] for c in chunks]
        print(f"Embedding {len(texts)} chunks...")
        embeddings = self.embedder.encode(texts, show_progress_bar=True, batch_size=32)
        embeddings = np.array(embeddings).astype("float32")

        # Normalize for cosine similarity
        faiss.normalize_L2(embeddings)

        # Build flat index (exact search, good for <100k chunks)
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)  # Inner Product = cosine sim after normalization
        self.index.add(embeddings)
        print(f"FAISS index built: {self.index.ntotal} vectors, dim={dim}")

    # ─── Main: Process Uploaded Files ────────────────────────────────────────
    def process_documents(self, uploaded_files) -> Dict:
        """Full pipeline: parse → chunk → embed → index."""
        all_chunks = []
        total_pages = 0
        doc_names = []

        for uploaded_file in uploaded_files:
            filename = uploaded_file.name
            doc_names.append(filename)
            file_bytes = uploaded_file.read()

            # Parse PDF
            pages = self.parse_pdf(file_bytes, filename)
            total_pages += len(pages)

            # Chunk each page
            for page_data in pages:
                chunks = self.chunk_text(
                    page_data["content"],
                    page_data["file"],
                    page_data["page"]
                )
                all_chunks.extend(chunks)

        self.chunks = all_chunks
        self.doc_names = doc_names

        # Build FAISS index
        self.build_index(all_chunks)

        return {
            "num_docs": len(uploaded_files),
            "num_chunks": len(all_chunks),
            "total_pages": total_pages,
            "doc_names": doc_names
        }

    # ─── Step 5: Retrieval ───────────────────────────────────────────────────
    def retrieve(self, query: str) -> List[Dict]:
        """Find top-k most relevant chunks for a query using FAISS."""
        query_embedding = self.embedder.encode([query]).astype("float32")
        faiss.normalize_L2(query_embedding)

        scores, indices = self.index.search(query_embedding, self.top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1:
                chunk = self.chunks[idx].copy()
                chunk["score"] = float(score)
                results.append(chunk)
        return results

    # ─── Step 6: LLM Generation ──────────────────────────────────────────────
    def generate_answer(self, query: str, context_chunks: List[Dict]) -> str:
        """Send query + retrieved context to LLM for answer generation."""
        
        # Build context string with source labels
        context_parts = []
        for i, chunk in enumerate(context_chunks):
            context_parts.append(
                f"[Source {i+1} - {chunk['file']}, Page {chunk['page']}]\n{chunk['content']}"
            )
        context = "\n\n---\n\n".join(context_parts)

        # Prompt template
        prompt = f"""You are a document intelligence assistant. Answer the question using ONLY the provided context.
Be specific, accurate, and cite which source(s) support your answer.
If the answer is not in the context, say "I couldn't find this information in the uploaded documents."

CONTEXT:
{context}

QUESTION: {query}

ANSWER (be clear and cite sources like [Source 1], [Source 2]):"""

        if self.provider == "groq":
            return self._call_groq(prompt)
        else:
            return self._call_gemini(prompt)

    def _call_groq(self, prompt: str) -> str:
        """Call Groq API (LLaMA model)."""
        from groq import Groq
        client = Groq(api_key=self.api_key)
        response = client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024,
            temperature=0.1
        )
        return response.choices[0].message.content

    def _call_gemini(self, prompt: str) -> str:
        """Call Google Gemini API."""
        import google.generativeai as genai
        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(self.model_name)
        response = model.generate_content(prompt)
        return response.text

    # ─── Full Query Pipeline ─────────────────────────────────────────────────
    def query(self, question: str) -> Dict[str, Any]:
        """
        Full RAG query:
        1. Retrieve relevant chunks
        2. Generate answer with citations
        3. Return answer + source metadata
        """
        if self.index is None:
            raise ValueError("No documents processed. Please upload and process documents first.")

        # Retrieve
        relevant_chunks = self.retrieve(question)

        # Generate
        answer = self.generate_answer(question, relevant_chunks)

        return {
            "answer": answer,
            "sources": relevant_chunks,
            "num_sources": len(relevant_chunks)
        }
