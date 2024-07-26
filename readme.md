# Project Overview

This project fetches academic content from various sources (Hindawi, MDPI, SpringerOpen, Arxiv, Elsevier) based on a query and generates an HTML report using Jinja2 templates.

## Usage


```python

if __name__ == '__main__':
    query = "FE model updating"
    sanitized_query = sanitize_filename(query)
    
    # Fetch records
    records_mdpi = fetch_mdpi_content(query)
    records_elsevier = fetch_elsevier_content(query)
    
    # Join records
    join_records = records_mdpi + records_elsevier + records_hind records_spring + records_arvix
    main(join_records, query)
    
```

## Functions

- `sanitize_filename(filename)`: Sanitize query string.
- `fetch_hindawi_content(query)`: Fetch from Hindawi.
- `fetch_mdpi_content(query)`: Fetch from MDPI.
- `fetch_springeropen_content(query)`: Fetch from SpringerOpen.
- `fetch_arxiv_content(query)`: Fetch from Arxiv.
- `fetch_elsevier_content(query)`: Fetch from Elsevier using Scopus API.
- `write_html_file(records, query)`: Render HTML template.
- `main(records, query)`: Generate HTML report.
