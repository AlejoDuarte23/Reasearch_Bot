from typing import List, TypeVar, Dict, Any, Callable
from pydantic import BaseModel


class Queryresults(BaseModel):
    query: str
    result: List[Dict[str, Any]] #make same types as the dicts

class Queryexcutor:
    def __init__(self, function_list: List[Callable]) -> None:
        function_list = self.function_list
    
    def execute(self, query: str) -> Queryresults:
        results = []

        return Queryresults(query=query, result=results)