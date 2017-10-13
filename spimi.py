import sys
from collections import OrderedDict

def spimi_invert(documents, block_size_limit):
    """ Applies the Single-pass in-memory indexing algorithm """
    block_number = 0
    dictionary = {} # (term-postingsList)
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
                temp_dict = sort_terms(dictionary)
                write_block_to_disk(temp_dict, block_number)
                temp_dict = {}
                block_number += 1
                dictionary = {}
    print("SPIMI invert complete!")

def sort_terms(termPostingslist):
    """ Sorts dictionary terms in alphabetical order """
    print(" -- Sorting terms...")
    sorted_dictionary = OrderedDict() # keep track of insertion order
    sorted_terms = sorted(termPostingslist)
    for term in sorted_terms:
        sorted_dictionary[term] = termPostingslist[term]
    return sorted_dictionary

def write_block_to_disk(termPostingslist, block_number):
    """ Writes index of the block (dictionary + postings list) to disk """
    print(" -- Writing term-positing list blocks...")
    # Define block
    base_path = 'index_blocks/'
    block_name = 'block-' + str(block_number) + '.txt'
    block = open(base_path + block_name, 'a+') # reading and writing
    # Write term : posting lists to block
    for index, term in enumerate(termPostingslist):
        # Term - Posting List Format
        # term:[docID1, docID2, docID3]
        # e.g. cat:[4,9,21,42]
        block.write(str(term) + ":" + str((termPostingslist[term])) + "\n")
    block.close()
