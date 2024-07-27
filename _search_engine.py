import requests
from bs4 import BeautifulSoup

# Query Hindawi
import requests
from bs4 import BeautifulSoup
import re
import urllib.parse
import xml.etree.ElementTree as ET


# %% hindawins
# Get metadata and content (Abstract, Conclusion)
def fetch_hindawi_content(query):
    search_url = f"https://www.hindawi.com/search/all/{query}/page/1/"
    response = requests.get(search_url)
    
    if response.status_code != 200:
        return "Failed to retrieve data"
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    records = []
    
    for element in soup.select('a[aria-label="Article Title"]'):
        href = element.get('href', 'N/A')
        
        title_elem = element.select_one('.article-card__title')
        title = title_elem.text.strip() if title_elem else 'N/A'
        
        article_url = f"https://www.hindawi.com{href}"
        article_response = requests.get(article_url)
        
        if article_response.status_code == 200:
            article_soup = BeautifulSoup(article_response.text, 'html.parser')
            
            # Abstract
            abstract_elem = article_soup.select_one('h4.header[id="abstract"]')
            if abstract_elem:
                abstract = abstract_elem.find_next_sibling('p')
                abstract_text = abstract.text if abstract else 'N/A'
            else:
                abstract_text = 'N/A'
            
            # Conclusion
            conclusion_elem = article_soup.find('h4', id=re.compile(r'conclusions', re.IGNORECASE))
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

    return records

#https://www.mdpi.com/search?sort=pubdate&page_count=200&year_from=1996&year_to=2024&q=Frequency+Domain+Decomposition&view=default
#https://www.mdpi.com/search?q=Frequency+Domain+Decomposition&journal=sensors
#https://www.mdpi.com/search?q=Modal+analysis&journal=buildings
# %% MDPI

def fetch_mdpi_content(query,journal):
    search_url = f"https://www.mdpi.com/search?q={query}&journal={journal}"
    response = requests.get(search_url)
    
    if response.status_code != 200:
        return "Failed to retrieve data"
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    records = []
    
    for element in soup.select('a.title-link'):
        href = element.get('href', 'N/A')
        title = element.text.strip() if element else 'N/A'
        
        article_url = f"https://www.mdpi.com{href}"
        article_response = requests.get(article_url)
        
        if article_response.status_code == 200:
            article_soup = BeautifulSoup(article_response.text, 'html.parser')
            
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

    return records


# %%  springeropen


def fetch_springeropen_content(query):
    search_url = f"https://www.springeropen.com/search?query={query}&searchType=publisherSearch"
    response = requests.get(search_url)
    
    if response.status_code != 200:
        return "Failed to retrieve data"
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    records = []
    
    for element in soup.select('a[data-test="title-link"]'):
        href = element.get('href', 'N/A').replace('//', 'https://')
        title = element.text.strip() if element else 'N/A'
        
        article_response = requests.get(href)
        
        if article_response.status_code == 200:
            article_soup = BeautifulSoup(article_response.text, 'html.parser')
            
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

    return records

#%% arvix 

def fetch_arxiv_content(query):
    formatted_query = urllib.parse.quote(query)
    url = f"https://export.arxiv.org/api/query?search_query=all:{formatted_query}&start=0&max_results=20"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request error occurred: {e}")
        return []

    root = ET.fromstring(response.content)
    
    records = []
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        title_elem = entry.find('{http://www.w3.org/2005/Atom}title')
        summary_elem = entry.find('{http://www.w3.org/2005/Atom}summary')
        id_elem = entry.find('{http://www.w3.org/2005/Atom}id')

        title = title_elem.text if title_elem is not None else 'N/A'
        summary = summary_elem.text if summary_elem is not None else 'N/A'
        href = id_elem.text if id_elem is not None else 'N/A'

        records.append({
            'title': title,
            'href': href,
            'abstract': summary,
            'conclusion': 'N/A'
        })

    return records


 # %% elsevier 
# %% imports 
import httpx
import json
import os

# %% scopus-paper get papers info

def scopus_paper_search(query, apikey):
    headers = {
        "X-ELS-APIKey": apikey,
        "Accept": 'application/json'
    }
    timeout = httpx.Timeout(10.0, connect=60.0)
    client = httpx.Client(timeout=timeout, headers=headers)
    url = f"https://api.elsevier.com/content/search/scopus?query={query}"
    r = client.get(url)
    print(r)
    return r.json()
# %% get abstract by doi 
def get_abstract_by_doi(doi, apikey):
    headers = {
        "X-ELS-APIKey": apikey,
        "Accept": 'application/json'
    }
    timeout = httpx.Timeout(10.0, connect=60.0)
    client = httpx.Client(timeout=timeout, headers=headers)
    url = f"https://api.elsevier.com/content/article/doi/{doi}"
    r = client.get(url)
    return r.json()

def get_abstract_by_eid(eid, apikey):
    headers = {
        "X-ELS-APIKey": apikey,
        "Accept": 'application/json'
    }
    timeout = httpx.Timeout(10.0, connect=60.0)
    client = httpx.Client(timeout=timeout, headers=headers)
    url = f"https://api.elsevier.com/content/abstract/eid/{eid}"
    
    r = client.get(url)
    return r.json()
def get_abstract_by_scopus_id(scopus_id, apikey):
    headers = {
        "X-ELS-APIKey": apikey,
        "Accept": 'application/json'
    }
    timeout = httpx.Timeout(10.0, connect=60.0)
    client = httpx.Client(timeout=timeout, headers=headers)
    url = f"https://api.elsevier.com/content/abstract/scopus_id/{scopus_id}"
    
    r = client.get(url)
    return r.json()



# %% get content

def fetch_elsevier_content(query):
    api_key =os.getenv('ELSEVIERAPI')

    records =[] 
    search_results = scopus_paper_search(query, api_key)
    print(search_results)
    entries = search_results['search-results']['entry']
    for entry in entries:
        try:
            _doi = entry['prism:doi']
            abstract_result = get_abstract_by_doi(_doi, api_key)
       
            abstract_content= abstract_result['full-text-retrieval-response']['coredata']
            abstract = abstract_content['dc:description']
            try:
                href = abstract_content['link'][1]['@href']
            except:
                href = abstract_content['@href']
                
            # href = abstract_content['@href']
            title = abstract_content['dc:title']
            records.append({
                'title': title,
                'href': href,
                'abstract': abstract,
                'conclusion': 'N/A'
            })
            print(f"fetch {title}")
        except:
            print('missmatch')
    return records

