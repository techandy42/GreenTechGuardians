from whoosh.index import open_dir
from whoosh.query import FuzzyTerm
from functools import reduce
from operator import and_
import streamlit as st

def load_index(index_dir):
    return open_dir(index_dir)


def search_index(query_str, index):
    with index.searcher() as searcher:
        # Parse each word in the query and apply the fuzzy search
        words = query_str.split()
        query = reduce(and_, [FuzzyTerm("title", word, maxdist=2, prefixlength=1) for word in words])
        results = searcher.search(query, limit=None)
        return [result['title'] for result in results]

index_dir = "indexdir"

# Load the index
index = load_index(index_dir)

# Streamlit UI
st.title("String Search")
query = st.text_input("Enter your search query:")

if query:
    results = search_index(query, index)
    st.write(results)
