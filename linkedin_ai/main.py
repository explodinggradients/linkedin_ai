
import json
import os
from typing import List
from mlflow import trace

from .document import Document
from .retrievers import BM25Retriever, VectorRetriever, BaseRetriever
from jinja2 import Environment, FileSystemLoader

base_dir = os.path.dirname(os.path.abspath(__file__))
prompt_path = os.path.join(base_dir, "prompts")

env = Environment(loader=FileSystemLoader(prompt_path))

class LinkedinAI:
    """Main RAG system for LinkedIn posts with factory methods for different retrieval strategies."""
    
    def __init__(
        self, 
        client,
        retriever: BaseRetriever,
        model: str = "gpt-4o",
        max_tokens: int = 1000,
        temperature: float = 0.1,
        verbose: bool = False
    ):
        self.retriever = retriever
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.client = client
    
    @classmethod
    def _load_posts(cls, file_path: str) -> List[Document]:
        """Load LinkedIn posts from a JSON file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Data file {file_path} not found")
        
        documents = []
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                posts_data = json.load(file)
                
            for post_id, post_info in posts_data.items():
                doc = Document(
                    id=post_id,
                    content=post_info.get("content", ""),
                    url=post_info.get("url", ""),
                    date=post_info.get("date", "unknown")
                )
                documents.append(doc)
                
            print(f"Loaded {len(documents)} LinkedIn posts")
            return documents
        except Exception as e:
            raise Exception(f"Error loading data: {e}")
    
    @classmethod
    async def from_bm25(
        cls,
        client,
        posts: str,
        model: str = "gpt-4o",
        top_k: int = 3,
        max_tokens: int = 1000,
        temperature: float = 0.1,
        verbose: bool = False
    ) -> "LinkedinAI":
        """Create a LinkedinAI instance using BM25 retrieval."""

        # Load documents
        documents = cls._load_posts(posts)
        
        # Create and initialize retriever
        retriever = BM25Retriever(documents, top_k)
        await retriever.initialize()
        
        return cls(client, retriever, model, max_tokens, temperature, verbose)
    
    @classmethod
    async def from_vector_search(
        cls,
        client,
        posts: str,
        embedding_model: str = "text-embedding-ada-002",
        model: str = "gpt-4o",
        top_k: int = 3,
        max_tokens: int = 1000,
        temperature: float = 0.1,
        verbose: bool = False
    ) -> "LinkedinAI":
        """Create a LinkedinAI instance using vector search retrieval."""
        # Initialize OpenAI client with Instructor
        
        # Load documents
        documents = cls._load_posts(posts)
    
        # Create vector file path
        vector_file = posts.replace(".json", "_vectors.npy")
        
        # Create and initialize retriever
        retriever = VectorRetriever(embedding_model, documents, top_k)
        # Pass the client during initialization
        await retriever.initialize(vector_file)
        
        return cls(client, retriever, model, max_tokens, temperature, verbose)
    
    @trace()
    async def ask(self, query: str, verbose: bool = False) -> str:
        """Answer a query using the RAG system."""
        if verbose:
            print(f"Query: {query}")
        
        # Retrieve relevant documents
        relevant_docs = await self.retriever.retrieve(query)
        
        if verbose:
            print(f"Retrieved {len(relevant_docs)} documents")
            for i, doc in enumerate(relevant_docs):
                print(f"Document {i+1}: {doc}")
        
        # Format context from retrieved documents
        context = "\n\n".join([
            f"Post {i+1} (Date: {doc.date}):\n{doc.content}\nURL: {doc.url}"
            for i, doc in enumerate(relevant_docs)
        ])
        
        # Generate answer using instructor and Pydantic model
        system_message = env.get_template("generation_prompt.txt").render()

        user_message = f"Posts:\n\n{context}\n\ Query: {query}"
        
        response = await self.client.chat.completions.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
        )
        
        
        return response.choices[0].message.content.strip()

