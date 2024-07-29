# Research Aggregator

A tool for querying and processing research data from various sources such as Arxiv, Mdpi, Springeropen, and Elsevier. The main functionality is encapsulated in the QueryExecutor class, which handles the asynchronous fetching and processing of data.


## Sources 
- Arvix: Fetch and process functions for Arxiv.
- Mdpi: Fetch and process functions for Mdpi, with specified journals.
- Springeropen: Fetch and process functions for Springeropen.
- Elsevier: Fetch and process functions for Elsevier (requires API).

Sources are defined with a fetch function and a process function as follow:

```python
from typing import Callable, Literal, Union
from pydantic import BaseModel

from .springer_open_functions import fetch_springeropen_content, process_data_springeropen
from .mdp_functions import fetch_mdpi_content, process_data_mdpi
from .arvix_functions import fetch_arvix_content, process_data_arvix
from .elsevier_functions_async import fetch_elsevier_content, process_data_elsevier

class Arvix(BaseModel):
    fetch_function: Callable = fetch_arvix_contents
    process_function: Callable = process_data_arvix

class Mdpi(BaseModel):
    fetch_function: Callable = fetch_mdpi_content
    process_function: Callable = process_data_mdpi
    journal: str = Literal['buildings', 'sensors', 'acoustics', 'algorithms', 'applmech', 'computation']

class Springeropen(BaseModel):
    fetch_function: Callable = fetch_springeropen_content
    process_function: Callable = process_data_springeropen

class Elsevier(BaseModel):
    fetch_function: Callable = fetch_elsevier_content
    process_function: Callable = process_data_elsevier

ResearchSource = Union[Arvix, Mdpi, Springeropen, Elsevier]
```
Go to classes.py for more details.


## Usage

```python

if __name__ == '__main__':

from research_aggregator import Arvix, Mdpi, Springeropen, Elsevier, QueryExecutor


if __name__ == "__main__":

    query = "Modal Analysis"

    sources = [
        Mdpi(journal="buildings"),
        Arvix(),
        Mdpi(journal="sensors"),
    ]

    executor = QueryExecutor(query=query, sources=sources)
    result = executor.search() # Queryresults
    print(result)
    
```


