
import asyncio

from typing import List, TypeVar, Dict, Any, Callable, Union, Literal
from pydantic import BaseModel

from .query_clases import Result, Queryresults
from .classes import ResearchSource, Mdpi

class QueryExecutor:
    def __init__(self, query: str, sources: List[ResearchSource]) -> None:
        self.sources = sources
        self.query = query

    def create_fetch_function(self) -> List[Callable]:
        list_of_fetch_functions = []

        for source in self.sources:
            if isinstance(source, Mdpi):
                fetch_function = lambda query, journal=source.journal: source.fetch_function(query, journal)
            else:
                fetch_function = source.fetch_function
            list_of_fetch_functions.append(fetch_function)

        return list_of_fetch_functions
    
    def create_process_function(self) -> List[Callable]:
        selected_sources = self.sources
        list_of_process_functions = []

        for source in selected_sources:
            process_function = source.process_function
            list_of_process_functions.append(process_function)
        return list_of_process_functions
    
    async def run_single_function(self, function:Callable ,query:str) -> Queryresults:
        query_results = await function(query)
        return query_results
    
    async def run_all_functions(self, functions:List[Callable], query:str) -> List[dict]:
        tasks = [self.run_single_function(function, query) for function in functions]
        return await asyncio.gather(*tasks)
    
    async def async_search(self)->Queryresults:
        query = self.query
        results = Queryresults(query=query, result=[])
        fetch_functions = self.create_fetch_function()
        process_functions = self.create_process_function()
        
        response_list  = await self.run_all_functions(fetch_functions, query)


        tasks = [
            processing_function(query, response)
            for processing_function, response in zip(process_functions, response_list)
        ]

        for task in tasks:
            async for record in task:
                print(record)
                results.add_result(Result(**record))
        
        return results
    
    def search(self):
        return asyncio.run(self.async_search())
        
