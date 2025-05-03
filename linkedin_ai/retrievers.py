import os
import re
import numpy as np
from typing import List
from mlflow import trace
from rank_bm25 import BM25Okapi
from abc import ABC, abstractmethod

from .document import Document

class BaseRetriever(ABC):
    """Abstract base class for document retrieval methods."""
    
    def __init__(self, documents: List[Document], top_k: int = 3):
        self.documents = documents
        self.top_k = top_k
    
    
    @abstractmethod
    async def retrieve(self, query: str) -> List[Document]:
        """Retrieve documents based on the query."""
        pass



class BM25Retriever(BaseRetriever):
    """BM25-based document retrieval."""
    
    def __init__(self, documents: List[Document], top_k: int = 3):
        super().__init__(documents, top_k)
        self.bm25 = None
        
    def preprocess_text(self, text: str) -> str:
        """Preprocess text for better indexing."""
        # Convert to lowercase
        text = text.lower()
        # Replace newlines with spaces
        text = re.sub(r'\n+', ' ', text)
        # Remove URLs
        text = re.sub(r'https?://\S+', '', text)
        # Remove special characters but keep spaces and alphanumerics
        text = re.sub(r'[^\w\s]', '', text)
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    async def initialize(self) -> None:
        """Initialize BM25 index for text retrieval."""
        if not self.documents:
            raise ValueError("No documents loaded. Please load data first.")
        
        # Tokenize documents for BM25
        tokenized_docs = []
        for doc in self.documents:
            processed_text = self.preprocess_text(doc.content)
            tokenized_docs.append(processed_text.split())
        
        # Create BM25 index
        self.bm25 = BM25Okapi(tokenized_docs)
        print("BM25 index initialized")
    
    @trace
    async def retrieve(self, query: str) -> List[Document]:
        """Retrieve relevant documents using BM25."""
        if not self.bm25:
            raise Exception("BM25 index not initialized")
        
        # Preprocess and tokenize the query
        processed_query = self.preprocess_text(query)
        query_tokens = processed_query.split()
        
        # Get BM25 scores
        doc_scores = self.bm25.get_scores(query_tokens)
        
        # Get indices of top k documents
        top_indices = np.argsort(doc_scores)[-self.top_k:][::-1]
        
        # Return top documents
        return [self.documents[i] for i in top_indices]


class VectorRetriever(BaseRetriever):
    """Vector-based document retrieval."""
    
    def __init__(self, client, model_name: str, documents: List[Document],top_k: int = 3):
        super().__init__(documents, top_k)
        self.model_name = model_name
        self.client = client
        self.document_vectors = None
    
    async def get_embedding(self, text: str) -> List[float]:
        """Get embedding for text using the OpenAI Embeddings API."""
        response = await self.client.embeddings.create(
            model=self.model_name,
            input=text,
        )
        
        return response.data[0].embedding
    
    async def initialize(self, vector_file: str = "vector_index.npy", verbose: bool=False) -> None:
        """Initialize vector search by creating embeddings for all documents."""
        
        if not self.documents:
            raise ValueError("No documents loaded. Please load data first.")
        
        # Check if vectors are already saved
        if os.path.exists(vector_file):
            self.document_vectors = np.load(vector_file)
            if verbose:
                print(f"Loaded existing document vectors from {vector_file}")
            # Assign vectors to documents
            for i, doc in enumerate(self.documents):
                doc.embedding = self.document_vectors[i].tolist()
            return
           
        
        # Generate embeddings for all documents
        embeddings = []
        for i, doc in enumerate(self.documents):
            if verbose:
                print(f"Generating embedding for document {i+1}/{len(self.documents)}...")
            embedding = await self.get_embedding(doc.content)
            doc.embedding = embedding
            embeddings.append(embedding)
        
        # Convert embeddings to numpy array for vector search
        self.document_vectors = np.array(embeddings)
        
        # Save embeddings to file
        np.save(vector_file, self.document_vectors)
        print(f"Saved document vectors to {vector_file}")
    
    @trace
    async def retrieve(self, query: str) -> List[Document]:
        """Retrieve relevant documents using vector similarity."""
        if self.document_vectors is None:
            raise Exception("Vector index not initialized")
        
        # Get query embedding
        query_embedding = await self.get_embedding(query)
        query_vector = np.array(query_embedding)
        
        # Calculate cosine similarity
        similarities = np.dot(self.document_vectors, query_vector) / (
            np.linalg.norm(self.document_vectors, axis=1) * np.linalg.norm(query_vector)
        )
        
        # Get indices of top k documents
        top_indices = np.argsort(similarities)[-self.top_k:][::-1]
        
        # Return top documents
        return [self.documents[i] for i in top_indices]
