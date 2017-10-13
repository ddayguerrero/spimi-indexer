import sys
import ast

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
    block = open(base_path + block_name, 'a+')
    # Write term : posting lists to block
    for index, term in enumerate(termPostingslist):
        # Term - Posting List Format
        # term:[docID1, docID2, docID3]
        # e.g. cat:[4,9,21,42]
        block.write(str(term) + ":" + str((termPostingslist[term])) + "\n")
    block.close()

def merge_blocks(blocks):
    """ Merges SPIMI blocks into final inverted index """
    empty_blocks = False
    spimi_index = open('spimi_inverted_index.txt', 'a+')
    # Collect sectioned (term : postings list) entries from SPIMI blocks
    temp_index = OrderedDict()
    for num, block in enumerate(blocks):
        line = blocks[num].readline() # term:[docID1, docID2, docID3]
        line_tpl = line.split(':')
        term = line_tpl[0]
        postings_list = ast.literal_eval(line_tpl[1])
        temp_index[num] = {term:postings_list}
    print(temp_index)
    # [{term: [postings list]}, blockID]
    tpl_block = ([[temp_index[i], i] for i in temp_index])
    # Fetch term postings list with the smallest alphabetical term
    firstmost_tpl = min(tpl_block, key=lambda t: list(t[0].keys()))
    # Extract term
    firstmost_tpl_term = (list(firstmost_tpl[0].keys())[0])
    print(firstmost_tpl_term)
    # Fetch all IDs of blocks which contain the same term in their sectioned (term: postings list)
    firstmost_tpl_block_ids = [block_id for block_id in temp_index if firstmost_tpl_term in [term for term in temp_index[block_id]]]
    print(firstmost_tpl_block_ids)

