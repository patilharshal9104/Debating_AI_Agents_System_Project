"""
evidence_retriever.py - RAG system for evidence retrieval
"""

from typing import List, Optional
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from web_loader import SimpleWebLoader

class EvidenceRetriever:
    def __init__(self):
        try:
            print("[DEBUG] Initializing HuggingFaceEmbeddings")
            model_kwargs = {'device': 'cpu'}
            encode_kwargs = {'normalize_embeddings': False}
            self.embedder = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs=model_kwargs,
                encode_kwargs=encode_kwargs
            )
            print("[DEBUG] Embedder initialized successfully")
        except Exception as e:
            print(f"[Embedding Error] Failed to initialize embedder: {e}")
            raise
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.vectorstore: Optional[FAISS] = None
    
    async def add_evidence(self, references: List[dict]) -> bool:
        """Add evidence from verified references to the vector store."""
        valid_urls = [ref.url for ref in references if ref.valid]
        if not valid_urls:
            print("[DEBUG] No valid URLs for evidence")
            return False
        
        try:
            print(f"[DEBUG] Loading {len(valid_urls)} URLs for RAG")
            loader = SimpleWebLoader(valid_urls)
            docs = await loader.aload()
            
            if not docs:
                print("[DEBUG] No documents loaded for RAG")
                return False
                
            splits = self.text_splitter.split_documents(docs)
            
            try:
                print("[DEBUG] Indexing documents with FAISS")
                if self.vectorstore is None:
                    self.vectorstore = FAISS.from_documents(splits, self.embedder)
                else:
                    self.vectorstore.add_documents(splits)
                print("[DEBUG] Documents indexed successfully")
                return True
            except Exception as e:
                print(f"[FAISS Error] Failed to index documents: {e}")
                return False
        except Exception as e:
            print(f"[RAG Error] Failed to add evidence: {e}")
            return False
    
    def get_relevant_evidence(self, query: str, k: int = 3) -> List[Document]:
        """Retrieve relevant evidence for a query."""
        if self.vectorstore is None:
            print("[DEBUG] No vectorstore available for evidence retrieval")
            return []
        print(f"[DEBUG] Retrieving evidence for query: {query[:50]}...")
        return self.vectorstore.similarity_search(query, k=k)