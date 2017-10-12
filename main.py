import sys
import reuters
from preprocess import *
from spimi import spimi_invert

def compileInvertedIndex(block_size_limit):
    """ Generate inverted index for Reuters21578 """
    reuters_corpus = reuters.ReutersCorpus()
    # Retrieve Reuters documents
    print("Retriving documents...")
    documents = reuters_corpus.retrieveDocuments()
    # Preprocessing documents
    print("Preprocessing documents...")
    documents = preprocess(documents)
    # Perform Single-pass in-memory (SPIMI) indexing
    print("Creating index - applying SPIMI...")
    spimi_invert(documents, block_size_limit)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        block_size_limit = int(sys.argv[1])
    else:
        block_size_limit = 10000 # default block size
    print(block_size_limit)
    compileInvertedIndex(block_size_limit)
