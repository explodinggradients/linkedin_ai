"""class to hold document"""

from typing import List, Optional
from pydantic import BaseModel, Field

class Document(BaseModel):
    """Pydantic model to represent a LinkedIn post as a document."""
    id: str
    content: str
    url: Optional[str] = None
    date: Optional[str] = None
    embedding: Optional[List[float]] = None
    
    def __str__(self):
        return f"Post {self.id}: {self.content}\n (Posted: {self.date})"


