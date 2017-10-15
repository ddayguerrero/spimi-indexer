""" Query handler for basic boolean retrieval """
import ast

from collections import OrderedDict
from vocabulary import normalize

def query():
    """ Setup query handler and execute query"""
    query = QueryHandler()
    user_input = input("Enter your boolean query using && or || exclusively: ")
    result_documents = query.execute(user_input)
    print("Boolean retrieval complete - Result:", result_documents)

def read_spimi_index():
    """ Reads and the SPIMI inverted index into memory"""
    print("Reading SPIMI index into memory...")
    spimi_index = OrderedDict()

    spimi_index_file = open('spimi_inverted_index.txt', 'r')
    # Construct SPIMI index
    # Term - Posting List Format
    # term:[docID1, docID2, docID3]
    # e.g. cat:[4,9,21,42]
    for line in spimi_index_file:
        if not line == '':
            line_tpl = line.rsplit(':', 1)
            term = line_tpl[0]
            postings_list = ast.literal_eval(line_tpl[1])
            spimi_index.update({term: postings_list})

    print("=============== Statistics ===============")
    print("Size of index:", len(spimi_index))
    non_positional_postings_count = 0
    for i in spimi_index:
        non_positional_postings_count += len(spimi_index[i])
    print("Number of non-positional postings: ", non_positional_postings_count)
    print("==========================================")

    return spimi_index

class QueryHandler:
    """Handles basic conjuction and disjunction boolean retrieval queries"""
    def __init__(self):
        self.spimi_index = read_spimi_index()

    def execute(self, queryInput):
        """Execute query"""
        # Parse input and determine type of boolean query
        if len(queryInput.strip().split()) == 1:
            print('--- Single Keyword Query')
            single_keyword = queryInput.strip().split()[0]
            print('--- Term:', single_keyword)
            if single_keyword in self.spimi_index:
                return self.spimi_index[single_keyword]
            else:
                print('No documents found!')
                return None
        else:
            and_index = queryInput.index('&&') if '&&' in queryInput else -1
            or_index = queryInput.index('||') if '||' in queryInput else -1
            if (and_index > 0) and (or_index < 0):
                query_type = 'AND'
                seperator = '&&'
            elif (or_index > 0) and (and_index < 0):
                query_type = 'OR'
                seperator = '||'
            else:
                print('Invalid query')
                return None

            # Extract terms and apply same preprocessing used for creating the SPIMI index
            query_terms = queryInput.strip().replace(" ", "").split(seperator)
            print('--- Multiple Keywords Query')
            terms = normalize(query_terms)
            print('--- Terms:', query_terms)

            # Collect postings lists of query terms
            tpls = []
            for term in terms:
                if term in self.spimi_index:
                    tpls.append(self.spimi_index[term])
                else:
                    tpls.append([])

            if query_type == 'AND':
                query_result = intersect(tpls)
                #query_result = set(tpl[0]).intersection(*tpl) # Intersection
            else:
                #query_result = sorted(list(set(tpls[0]).union(*tpls))) # Union
                query_result = union(tpls)
            return query_result

def intersect(term_postings_lists):
    """ Computes conjunctive queries for the set of tls containing the input list of terms """
    if len(term_postings_lists) < 2:
        return None
    sort_doc_tpl = sorted(term_postings_lists)
    sort_length_tpl = sorted(sort_doc_tpl, key=len)
    result = min(term_postings_lists, key=len) # shortest
    remainder = sort_length_tpl[1:]
    print("result", result)
    print("remainder", remainder)
    if not remainder:
        remainder = None
    if not result:
        result = None
    while not remainder is None and not result is None:
        result = intersect_rest(result, remainder[0])
        print("result", result)
        remainder = remainder[1:]
        print("remainder", remainder)
        if not remainder:
            remainder = None
    return result

def intersect_rest(tpl1, tpl2):
    """ Computes intersection between two term postings list"""
    answer = []
    iter_tpl1 = iter(tpl1)
    iter_tpl2 = iter(tpl2)
    doc_id1 = next(iter_tpl1, None)
    doc_id2 = next(iter_tpl2, None)
    while not doc_id1 is None and not doc_id2 is None:
        if doc_id1 == doc_id2:
            answer.append(doc_id1)
            doc_id1 = next(iter_tpl1, None)
            doc_id2 = next(iter_tpl2, None)
        elif doc_id1 < doc_id2:
            doc_id1 = next(iter_tpl1, None)
        else:
            doc_id2 = next(iter_tpl2, None)
    print("Intersection of two", answer)
    if not answer:
        return None
    return answer

def union(term_postings_lists):
    """ Computes disjunctive queries for the set of tls containing the input list of terms """
    sort_doc_tpl = sorted(term_postings_lists)
    sort_length_tpl = sorted(sort_doc_tpl, key=len)
    result = min(term_postings_lists, key=len)
    remainder = sort_length_tpl[1:]
    print("result", result)
    print("remainder", remainder)
    if not remainder:
        remainder = None
    if not result:
        result = None
    while not remainder is None:
        result = union_rest(result, remainder[0])
        print("result", result)
        remainder = remainder[1:]
        print("remainder", remainder)
        if not remainder:
            remainder = None
    return result

def union_rest(tpl1, tpl2):
    """ Computes union between two term postings list """
    answer = []
    if not tpl1:
        doc_id1 = None
    else:
        iter_tpl1 = iter(tpl1)
        doc_id1 = next(iter_tpl1, None)
    if not tpl2:
        doc_id2 = None
    else:
        iter_tpl2 = iter(tpl2)
        doc_id2 = next(iter_tpl2, None)
    while not doc_id1 is None or not doc_id2 is None:
        if doc_id1 is None:
            answer.append(doc_id2)
            doc_id2 = next(iter_tpl2, None)
        elif doc_id2 is None:
            answer.append(doc_id1)
            doc_id2 = next(iter_tpl2, None)
        elif doc_id1 == doc_id2:
            answer.append(doc_id1)
            doc_id1 = next(iter_tpl1, None)
            doc_id2 = next(iter_tpl2, None)
        elif doc_id1 < doc_id2:
            answer.append(doc_id1)
            doc_id1 = next(iter_tpl1, None)
        else:
            answer.append(doc_id2)
            doc_id2 = next(iter_tpl2, None)
    print("Union of two", answer)
    if not answer:
        return None
    return answer

if __name__ == '__main__':
    query()
