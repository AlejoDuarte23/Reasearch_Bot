
from typing import List, TypeVar, Dict, Any, Callable, Union, Literal, Optional
from pydantic import BaseModel, Field

from .springer_open_functions import fetch_springeropen_content, process_data_springeropen
from .mdp_functions import fetch_mdpi_content, process_data_mdpi
from .arvix_functions import fetch_arvix_content, process_data_arvix
from .elsevier_functions_async import fetch_elsevier_content, process_data_elsevier





class Arvix(BaseModel):
    fetch_function: Callable = fetch_arvix_content
    process_function: Callable = process_data_arvix

    
class Mdpi(BaseModel):
    fetch_function: Callable = fetch_mdpi_content
    process_function: Callable = process_data_mdpi 
    journal: str = Literal['buildings', "sensors", "acoustics", "algorithms", "applmech","computation"]
    

class Springeropen(BaseModel):  
    fetch_function: Callable = fetch_springeropen_content
    process_function: Callable = process_data_springeropen

class Elsevier(BaseModel): 
    fetch_function: Callable = fetch_elsevier_content
    process_function: Callable = process_data_elsevier

ResearchSource = Union[Arvix, Mdpi, Springeropen, Elsevier]