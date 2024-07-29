
import aiohttp.web_response
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import List, Callable, AsyncGenerator, Optional


import aiohttp.web_response
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import List, Callable, AsyncGenerator, Optional



async def fetch_url(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def fetch_springeropen_content(query):
    search_url = f"https://www.springeropen.com/search?query={query}&searchType=publisherSearch"
    response = await fetch_url(search_url)
    return response 


async def process_data_springeropen( query , response: str)->AsyncGenerator[dict, None]:
    soup = BeautifulSoup(response, 'html.parser')
    records = []
    
    for element in soup.select('a[data-test="title-link"]'):
        try:
            href = element.get('href', 'N/A').replace('//', 'https://')
            title = element.text.strip() if element else 'N/A'
            
            article_response = await fetch_url(href)
            
            if article_response:
                article_soup = BeautifulSoup(article_response, 'html.parser')
                
                # Abstract
                abstract_elem = article_soup.select_one('div[id="Abs1-content"]')
                abstract_text = abstract_elem.p.text if abstract_elem and abstract_elem.p else 'N/A'
                
                # Conclusion or Summary
                conclusion_elem = article_soup.find('h2', class_='c-article-section__title', string=re.compile(r'.*(conclusion|summary).*', re.IGNORECASE))
                if conclusion_elem:
                    conclusion_text = ' '.join([p.text for p in conclusion_elem.find_all_next('p', limit=5)])
                else:
                    conclusion_text = 'N/A'
                
                record = {
                    'href': href,
                    'title': title,
                    'abstract': abstract_text,
                    'conclusion': conclusion_text
                }
                yield record
        except:
            print('Error')
