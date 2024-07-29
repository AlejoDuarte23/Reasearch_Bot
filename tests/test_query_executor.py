import sys
sys.path.append('..')

from research_aggregator import Arvix, Mdpi, Springeropen, Elsevier, QueryExecutor


if __name__ == "__main__":

    query = "Modal Analysis"

    sources = [
        Mdpi(journal="buildings"),
        Arvix(),
        Mdpi(journal="sensors"),
    ]

    executor = QueryExecutor(query=query, sources=sources)
    result = executor.search()
    print(result)