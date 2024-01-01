import os.path
import requests
from download import download_wikipedia_abstracts
from load import load_documents
from search.timing import timing
from search.index import Index

@timing
def index_documents(documents, index):
    for i, document in enumerate(documents):
        index.index_document(document)
        if i % 5000 == 0:
            print(f'Indexed {i} documents', end='\r')
    return index

if __name__ == '__main__':
    if not os.path.exists('data/enwiki-latest-abstract.xml.gz'):
        download_wikipedia_abstracts()

    index = index_documents(load_documents(), Index())
    print(f'Index contains {len(index.documents)} documents')

    # Perform searches
    search_results_and = index.search('Artificial Intelligence', search_type='AND', rank=True)[:5]
    search_results_or = index.search('Artificial Intelligence', search_type='OR', rank=True)[:5]

    # Print search results
    print('\nSearch Results (AND):\n')
    for rank, result in enumerate(search_results_and, 1):
        abstract, score = result
        print(f'Rank: {rank}')
        print(f'Title: {abstract.title}')
        print(f'Score: {score}')
        print(f'Abstract: {abstract.abstract}')
        print(f'URL: {abstract.url}\n')

    print('\nSearch Results (OR):\n')
    for rank, result in enumerate(search_results_or, 1):
        abstract, score = result
        print(f'Rank: {rank}')
        print(f'Title: {abstract.title}')
        print(f'Score: {score}')
        print(f'Abstract: {abstract.abstract}')
        print(f'URL: {abstract.url}\n')
