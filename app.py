from _report_engine_jinja import main , sanitize_filename
from _search_engine import (fetch_elsevier_content,
                            fetch_hindawi_content,
                            fetch_mdpi_content,
                            fetch_springeropen_content,
                            fetch_arxiv_content)


if __name__ == '__main__':
    query = "Enhanced Frequency Domain Decomposition"
    sanitized_query = sanitize_filename(query)

    records_mdpi = fetch_mdpi_content(query , journal='buildings')
    records_spring = fetch_springeropen_content(query)
    records_arvix = fetch_arxiv_content(query)
    records_elsevier = fetch_elsevier_content(query)
    # Join records
    join_records =  records_elsevier + records_arvix
    main(join_records, query)
