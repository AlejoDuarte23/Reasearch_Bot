from pydantic import BaseModel, Field
from typing import List, Optional
import uuid

class Result(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    href: str
    title: str
    abstract: str
    conclusion: str
    
class Queryresults(BaseModel):
    query: str
    result: List[Result]
    
    def add_result(self, result: Result):
        self.result.append(result)