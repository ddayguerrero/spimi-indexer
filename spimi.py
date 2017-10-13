import sys
import ast
import re

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
        result = [int(docIds) for docIds in termPostingslist[term]]
        sorted_dictionary[term] = result
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
    merge_completed = False
    spimi_index = open('spimi_inverted_index.txt', 'a+')
    # Collect sectioned (term : postings list) entries from SPIMI blocks
    temp_index = OrderedDict()
    for num, block in enumerate(blocks):
        print("-- Reading into memory...", blocks[num].name)
        line = blocks[num].readline() # term:[docID1, docID2, docID3]
        line_tpl = line.split(':')
        term = line_tpl[0]
        postings_list = ast.literal_eval(line_tpl[1])
        temp_index[num] = {term:postings_list}
    while not merge_completed:
        # [{term: [postings list]}, blockID]
        tpl_block = ([[temp_index[i], i] for i in temp_index])
        # Fetch the current term postings list with the smallest alphabetical term
        smallest_tpl = min(tpl_block, key=lambda t: list(t[0].keys()))
        # Extract the smallest term
        smallest_tpl_term = (list(smallest_tpl[0].keys())[0])
        # Fetch all IDs of blocks which contain the same term in their sectioned (term: postings list)
        # For every block, check if smallest term is in the array of terms from all blocks
        smallest_tpl_block_ids = [block_id for block_id in temp_index if smallest_tpl_term in [term for term in temp_index[block_id]]]
        # Build a new postings list which contains all postings related to the current smallest term
        # Flatten the array of postings and sort
        smallest_tpl_pl = sorted(sum([pl[smallest_tpl_term] for pl in (temp_index[block_id] for block_id in smallest_tpl_block_ids)], []))

        spimi_index.write(str(smallest_tpl_term) + ":" + str(smallest_tpl_pl) + "\n")

        # Collect the next sectioned (term : postings list) entries from blocks that contained the previous smallest tpl term
        for block_id in smallest_tpl_block_ids:
            # Read the blocks and read tpl in a temporary index
            block = [file for file in blocks if re.search('block-'+str(block_id), file.name)]
            if block[0]:
                line = block[0].readline()
                if not line == '':
                    line_tpl = line.split(':')
                    term = line_tpl[0]
                    postings_list = ast.literal_eval(line_tpl[1])
                    temp_index[block_id] = {term:postings_list}
                else:
                    # Delete block entry from the temporary sectioned index holder if no line found
                    del temp_index[block_id]
                    blocks.remove(block[0])
                    print("Finished merging block:", block[0].name)
            else:
                blocks.remove(block[0])
        # If all block IO streams have been merged
        if not blocks:
            merge_completed = True
            print("SPIMI completed! All blocks merged into final index: spimi_inverted_index.txt")
    return 0
