""" Query handler for basic boolean retrieval """
import ast
import math
from collections import OrderedDict
import reuters
from vocabulary import normalize, preprocess

def retrieve_result_set():
    """ Setup query handler and execute query """
    user_input = input("Enter your boolean query using && or || exclusively: ")
    result_query, result_documents = QUERYHANDLER.execute(user_input)
    return result_query, result_documents

def query_boolean():
    """ Setup query handler and execute query """
    result_query, result_documents = retrieve_result_set()
    print("Boolean retrieval complete - Result:", result_documents)
    if not result_documents is None:
        num_results = len(result_documents)
        print("Amount of documents found:", num_results)

def query_bm25():
    """ Setup BM25 ranking algorithm """
    result_query, result_documents = retrieve_result_set()
    if not result_documents is None:
        document_scores = QUERYHANDLER.compute_bm25(result_query, result_documents)
        for key, value in document_scores:
            print("Document: %s - Score: %s" % (key, value))


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
        print("Retriving corpus documents into memory... ")
        reuters_corpus = reuters.ReutersCorpus()
        self.documents = preprocess(reuters_corpus.retrieveDocuments())

    def compute_bm25(self, query, documents):
        """ Okapi-BM25: rank documents according to their relevance to a given query """
        print(("====================== Okapi-BM25 ======================="))
        result_scores = OrderedDict()
        l_ave = sum(len(document) for document in self.documents) / len(self.documents) # average length of all documents
        # print("l_ave", l_ave)
        n = len(self.documents) # number of documents in the reuteurs corpus
        # print("N", n)
        for doc_id in documents:
            # print("doc_id", doc_id[0])
            l_d = len(self.documents[str(doc_id[0])]) # length of document d
            # print("l_d", l_d)
            for term in query:
                dft = len(self.spimi_index[term]) # document frequency of term
                idf = compute_idf(n, dft) # inverse document frequency
                tf = 0 # term frequency of term in document
                if doc_id in self.spimi_index[term]:
                    tf = doc_id[1]
                tftd = compute_tftd_normalized(l_d, l_ave, tf) # normalize tftd
                if doc_id[0] in result_scores:
                    result_scores[doc_id[0]] += (idf * tftd)
                else:
                    result_scores[doc_id[0]] = (idf * tftd)
        result_scores = sorted(result_scores.items(), key=lambda x:x[1], reverse=True) # sort documents by decreasing score value
        return result_scores

    def execute(self, queryInput):
        """Execute query"""
        # Parse input and determine type of boolean query
        if len(queryInput.strip().split()) == 1:
            print('--- Single Keyword Query')
            single_keyword = queryInput.strip().split()[0]
            print('--- Term:', single_keyword)
            single_keyword_normalized = normalize([single_keyword])
            keyword = single_keyword_normalized[0]
            if keyword in self.spimi_index:
                return single_keyword_normalized, self.spimi_index[keyword]
            else:
                print('No documents found!')
                return single_keyword_normalized, None
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
                print('Invalid query!')
                return None, None

            # Extract terms and apply same preprocessing used for creating the SPIMI index
            query_terms = queryInput.strip().replace(" ", "").split(seperator)
            print('--- Multiple Keyword Query')
            terms = normalize(query_terms)
            print('--- Terms:', query_terms)

            # Collect postings lists of query terms
            tpls = []
            for term in terms:
                if term in self.spimi_index:
                    tpls.append(self.spimi_index[term])
                    # print(term, self.spimi_index[term])
                else:
                    tpls.append([])
            if query_type == 'AND':
                query_result = intersect(tpls)
                #query_result = set(tpl[0]).intersection(*tpl) # Intersection
            else:
                #query_result = sorted(list(set(tpls[0]).union(*tpls))) # Union
                query_result = union(tpls)
            return terms, query_result

def compute_idf(n, dft):
    """ Measure of how much information the word provides:
    whether the term is common or rare across all documents """
    return math.log(n/dft)

def compute_tftd_normalized(l_d, l_ave, tf):
    """ Computes the count of a term in a document:
    the number of times that term t occurs in document d """
    k1 = 1.5 # term frequency scaling - how relevant tf is to the overall score
    b1 = 0.75 # length normalization constant - scaling the term weight by document length
    tftd = ((k1 + 1) * tf) / ((k1 * ((1-b1) + b1 * (l_d/l_ave))) + tf) # normalize
    return tftd

def intersect(term_postings_lists):
    """ Computes conjunctive queries for the set of tls containing the input list of terms """
    if len(term_postings_lists) < 2:
        return None
    sort_doc_tpl = sorted(term_postings_lists)
    sort_length_tpl = sorted(sort_doc_tpl, key=len)
    result = min(term_postings_lists, key=len) # shortest
    remainder = sort_length_tpl[1:]
    # print("result", result)
    # print("remainder", remainder)
    if not remainder:
        remainder = None
    if not result:
        result = None
    while not remainder is None and not result is None:
        result = intersect_rest(result, remainder[0])
        # print("result", result)
        remainder = remainder[1:]
        # print("remainder", remainder)
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
        if doc_id1[0] == doc_id2[0]:
            answer.append(doc_id1)
            doc_id1 = next(iter_tpl1, None)
            doc_id2 = next(iter_tpl2, None)
        elif doc_id1[0] < doc_id2[0]:
            doc_id1 = next(iter_tpl1, None)
        else:
            doc_id2 = next(iter_tpl2, None)
    # print("Intersection of two", answer)
    if not answer:
        return None
    return answer

def union(term_postings_lists):
    """ Computes disjunctive queries for the set of tls containing the input list of terms """
    sort_doc_tpl = sorted(term_postings_lists)
    sort_length_tpl = sorted(sort_doc_tpl, key=len)
    result = min(term_postings_lists, key=len)
    remainder = sort_length_tpl[1:]
    # print("result1", result)
    # print("remainder1", remainder)
    if not remainder:
        remainder = None
    if not result:
        result = None
    while not remainder is None:
        result = union_rest(result, remainder[0])
        # print("result2", result)
        remainder = remainder[1:]
        # print("remainder2", remainder)
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
    # print("doc_id1", doc_id1)
    # print("doc_id2", doc_id2)
    while not doc_id1 is None or not doc_id2 is None:
        # print("doc_id3", doc_id1)
        # print("doc_id3", doc_id2)
        if doc_id1 is None:
            answer.append(doc_id2)
            doc_id2 = next(iter_tpl2, None)
        elif doc_id2 is None:
            answer.append(doc_id1)
            doc_id1 = next(iter_tpl1, None)
        elif doc_id1[0] == doc_id2[0]:
            answer.append(doc_id1)
            doc_id1 = next(iter_tpl1, None)
            doc_id2 = next(iter_tpl2, None)
        elif doc_id1[0] < doc_id2[0]:
            answer.append(doc_id1)
            doc_id1 = next(iter_tpl1, None)
        else:
            answer.append(doc_id2)
            doc_id2 = next(iter_tpl2, None)
    # print("Union of two", answer)
    if not answer:
        return None
    return answer

if __name__ == '__main__':
    QUERYHANDLER = QueryHandler()
    while True:
        QUERYTYPE = input("Please select your type of query? (0 - Boolean or 1 - BM25) : ")
        if QUERYTYPE == '0':
            print("Boolean")
            query_boolean()
        elif QUERYTYPE == '1':
            print("BM25")
            query_bm25()
        else:
            print("Please enter a valid type...")
