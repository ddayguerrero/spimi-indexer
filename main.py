import sys
import reuters
from preprocess import preprocess
from spimi import spimi_invert

def compileInvertedIndex(block_size_limit):
    """ Generate inverted index for Reuters21578 """
    reuters_corpus = reuters.ReutersCorpus()
    # Retrieve Reuters documents
    print("=============== Retriving documents... =============== ")
    documents = reuters_corpus.retrieveDocuments()
    # Preprocessing documents
    print("=============== Preprocessing documents... ===============")
    documents = preprocess(documents)
    # Perform Single-pass in-memory (SPIMI) indexing
    print("=============== Applying SPIMI... ===============")
    spimi_invert(documents, block_size_limit)
    # Merge blocks into final index
    print("=============== Merging SPIMI blocks into final inverted index... ===============")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        block_size_limit = int(sys.argv[1])
    else:
        block_size_limit = 1000000 #250000 # default block size (in bytes)
    print(block_size_limit)
    compileInvertedIndex(block_size_limit)
