import sys
from os import listdir

import reuters
from vocabulary import preprocess
from spimi import spimi_invert, merge_blocks

def compile_inverted_index(block_size_limit):
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
    spimi_blocks = [open('index_blocks/'+block) for block in listdir('index_blocks/')]
    merge_blocks(spimi_blocks)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        block_size_limit = int(sys.argv[1])
    else:
        block_size_limit = 250000 # default block size (in bytes)
        # block_size_limit = 1000000 # default block size (in bytes)
    print(block_size_limit)
    compile_inverted_index(block_size_limit)