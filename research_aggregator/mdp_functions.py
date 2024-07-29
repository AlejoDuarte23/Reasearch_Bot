import aiohttp.web_response
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import List, Callable, AsyncGenerator, Optional
import re



async def fetch_url(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
        
async def fetch_mdpi_content(query,journal='buildings'):
    search_url = f"https://www.mdpi.com/search?q={query}&journal={journal}"
    response = await fetch_url(search_url)
    return response

async def process_data_mdpi( query , response: str)->AsyncGenerator[dict, None]:
    soup = BeautifulSoup(response, 'html.parser')
    
    records = []
    
    for element in soup.select('a.title-link'):
        href = element.get('href', 'N/A')
        title = element.text.strip() if element else 'N/A'
        
        article_url = f"https://www.mdpi.com{href}"
        article_response = await fetch_url(article_url)
        
        if article_response:
            article_soup = BeautifulSoup(article_response, 'html.parser')
            
            # Abstract
            abstract_elem = article_soup.select_one('h2[id="html-abstract-title"]')
            if abstract_elem:
                abstract = abstract_elem.find_next_sibling('div', class_='html-p')
                abstract_text = abstract.text if abstract else 'N/A'
            else:
                abstract_text = 'N/A'
            
            # Conclusion
            conclusion_elem = article_soup.find('h2', string=re.compile(r'.*conclusion.*', re.IGNORECASE))
            if conclusion_elem: 
                conclusion_text = ' '.join([p.text for p in conclusion_elem.find_all_next('div', class_='html-p', limit=5)])
            else:
                conclusion_text = 'N/A'
            
            record = {
                'href': href,
                'title': title,
                'abstract': abstract_text,
                'conclusion': conclusion_text
            }

            yield record