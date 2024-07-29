import aiohttp.web_response
import aiohttp
from bs4 import BeautifulSoup
from typing import List, Callable, AsyncGenerator, Optional

import urllib.parse
import xml.etree.ElementTree as ET



async def fetch_url(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def fetch_arvix_content(query):   
    formatted_query = urllib.parse.quote(query)
    search_url = f"https://export.arxiv.org/api/query?search_query=all:{formatted_query}&start=0&max_results=20"
    response = await fetch_url(search_url)
    return response


async def process_data_arvix(query , response: str)->AsyncGenerator[dict, None]:
    response_parse = ET.fromstring(response)

    for entry in response_parse.findall('{http://www.w3.org/2005/Atom}entry'):
        title_elem = entry.find('{http://www.w3.org/2005/Atom}title')
        summary_elem = entry.find('{http://www.w3.org/2005/Atom}summary')
        id_elem = entry.find('{http://www.w3.org/2005/Atom}id')

        title = title_elem.text if title_elem is not None else 'N/A'
        summary = summary_elem.text if summary_elem is not None else 'N/A'
        href = id_elem.text if id_elem is not None else 'N/A'
        record = {
            'href': href,
            'title': title,
            'abstract': summary,
            'conclusion': 'N/A'
        }
        yield record
