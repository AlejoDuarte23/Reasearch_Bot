import asyncio
import aiohttp
from typing import List, Callable
from bs4 import BeautifulSoup

import httpx
import json
import os
import re


async def fetch_url(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


# %%  springeropen
async def fetch_springeropen_content(query):
    search_url = f"https://www.springeropen.com/search?query={query}&searchType=publisherSearch"
    response = await fetch_url(search_url)
        
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
                
                records.append({
                    'href': href,
                    'title': title,
                    'abstract': abstract_text,
                    'conclusion': conclusion_text
                })
        except Exception as e:
            print(e)
        
    print(f"finish with {len(records)} records")

    return records


async def fetch_mdpi_content(query,journal='buildings'):
    search_url = f"https://www.mdpi.com/search?q={query}&journal={journal}"
    response = await fetch_url(search_url)
    
    if not response:
        return "Failed to retrieve data"
        
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
            
            records.append({
                'href': href,
                'title': title,
                'abstract': abstract_text,
                'conclusion': conclusion_text
            })
    print(f"finish with {len(records)} records")

    return records


async def run_single_function(function:Callable ,query:str) -> List[dict]:
    records = await function(query)
    return records


async def run_all_functions(functions:List[Callable], query:str) -> List[dict]:
    tasks = [run_single_function(function, query) for function in functions]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    concurrent = False
    test = True

    if concurrent:
        query = "Model Updating"
        functions = [fetch_mdpi_content, fetch_springeropen_content]
        asyncio.run(run_all_functions(functions, query))

    if test:
        asyncio.run(run_single_function(fetch_springeropen_content, "Model Updating"))
