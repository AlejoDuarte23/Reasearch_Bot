import aiohttp
import asyncio
import json
import os

from typing import List, Callable, AsyncGenerator, Optional

async def scopus_paper_search(query, apikey):
    headers = {
        "X-ELS-APIKey": apikey,
        "Accept": 'application/json'
    }
    url = f"https://api.elsevier.com/content/search/scopus?query={query}"
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as r:
            print(r)
            return await r.json()

# %% get abstract by doi 
async def get_abstract_by_doi(doi, apikey):
    headers = {
        "X-ELS-APIKey": apikey,
        "Accept": 'application/json'
    }
    url = f"https://api.elsevier.com/content/article/doi/{doi}"
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as r:
            return await r.json()

async def get_abstract_by_eid(eid, apikey):
    headers = {
        "X-ELS-APIKey": apikey,
        "Accept": 'application/json'
    }
    url = f"https://api.elsevier.com/content/abstract/eid/{eid}"
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as r:
            return await r.json()

async def get_abstract_by_scopus_id(scopus_id, apikey):
    headers = {
        "X-ELS-APIKey": apikey,
        "Accept": 'application/json'
    }
    url = f"https://api.elsevier.com/content/abstract/scopus_id/{scopus_id}"
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as r:
            return await r.json()

async def fetch_elsevier_content(query):
    api_key = os.getenv('ELSEVIERAPI')
    search_results = await scopus_paper_search(query, api_key)
    return search_results

async def process_data_elsevier(query, response: json)->AsyncGenerator[dict, None]:
    api_key = os.getenv('ELSEVIERAPI')

    entries = response['search-results']['entry']
    for entry in entries:
        try:
            _doi = entry['prism:doi']
            abstract_result = await get_abstract_by_doi(_doi, api_key)
       
            abstract_content = abstract_result['full-text-retrieval-response']['coredata']
            abstract = abstract_content['dc:description']
            try:
                href = abstract_content['link'][1]['@href']
            except:
                href = abstract_content['@href']
                
            title = abstract_content['dc:title']
            records={
                'title': title,
                'href': href,
                'abstract': abstract,
                'conclusion': 'N/A'
            }
            print(f"fetch {title}")
           
            yield records
       
        except Exception as e:
            print(f'missmatch: {e}')

async def main():
    query = "Modal analysis"
    records = await fetch_elsevier_content(query)
    print(records)

async def testing_elsevier():
    query = "System identification OMA"
    response = await fetch_elsevier_content(query)
    async for record in process_data_elsevier(query, response):
        print(record)



