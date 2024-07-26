from _report_engine_jinja import main , sanitize_filename
from _search_engine import (fetch_elsevier_content,
                            fetch_hindawi_content,
                            fetch_mdpi_content,
                            fetch_springeropen_content,
                            fetch_arxiv_content)


if __name__ == '__main__':
    query = "FE model updating"
    sanitized_query = sanitize_filename(query)
    
    # Fetch records
    records_hind = fetch_hindawi_content(query)
    records_mdpi = fetch_mdpi_content(query)
    #records_spring = fetch_springeropen_content(query)
    records_arvix = fetch_arxiv_content(query)
    records_elsevier = fetch_elsevier_content(query)
    # Join records
    join_records =  records_mdpi + records_elsevier #records_hind# +records_spring
    main(join_records, query)
