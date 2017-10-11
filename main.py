import sys
import reuters
from preprocess import *

def compileInvertedIndex():
    """ Generate inverted index for Reuters21578 """
    reuters_corpus = reuters.ReutersCorpus()
    # Retrieve Reuters documents
    print("Retriving documents...")
    documents = reuters_corpus.retrieveDocuments()
    # Preprocessing documents
    print("Preprocessing documents...")
    preprocess(documents)

if __name__ == '__main__':
    compileInvertedIndex()
