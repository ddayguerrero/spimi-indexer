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
    # while True: # keep running the program
    #     docID_input = input("Enter document ID for lookup:")
    #     print("You entered:", docID_input)
    #     print(documents[docID_input])

if __name__ == '__main__':
    if len(sys.argv) > 1:
        block_size_limit = int(sys.argv[1])
    else:
        # block_size_limit = 250000 # default block size (in bytes)
        block_size_limit = 750000 # default block size (in bytes) 0.75 MB
    print("Current block size limit: ", block_size_limit)
    compile_inverted_index(block_size_limit)
    