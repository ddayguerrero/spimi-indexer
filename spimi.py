import sys
from collections import OrderedDict
def spimi_invert(documents, block_size_limit):
    """ Applies Single-pass in-memory indexing algorithm """
    dictionary = {}
    for index, docID in enumerate(documents):
        for term in documents[docID]:
            # If term occurs for the first time
            if term not in dictionary:
                # Add term to dictionary, create new postings list, and add docID
                dictionary[term] = [docID]
            else:
                # If term has a subsequent occurence
                if docID not in dictionary[term]:
                    # Add a posting (docID) to the existing posting list of the term
                    dictionary[term].append(docID)
        if sys.getsizeof(dictionary) > block_size_limit:
            # sort and write dictionary to block
            dictionary = sort_terms(dictionary)
            write_block_to_disk(dictionary)
    print(dictionary)

def sort_terms(dictionary):
    """ Sorts dictionary terms in alphabetical order """
    sorted_dictionary = OrderedDict()
    sorted_terms = sorted(dictionary)
    for term in sorted_terms:
        sorted_dictionary[term] = dictionary[term]
    return sorted_dictionary

def write_block_to_disk(dictionary):
    """ Writes index of the block (dictionary + postings list) to disk """

