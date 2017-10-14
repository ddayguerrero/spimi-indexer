import ast

from collections import OrderedDict
from vocabulary import normalize

def query():
    """ Setup query handler and execute query"""
    query = QueryHandler()
    user_input = input("Enter your boolean query using && or || exclusively:")
    result = query.execute(user_input)
    print("Boolean retrieval complete! Result: ", result)

def read_spimi_index():
    """ Reads and the SPIMI inverted index into memory"""
    print("Reading SPIMI index into memory...")
    spimi_index = OrderedDict()

    spimi_index_file = open('spimi_inverted_index.txt', 'r')
    for line in spimi_index_file:
        if not line == '':
            line_tpl = line.split(':')
            term = line_tpl[0]
            postings_list = ast.literal_eval(line_tpl[1])
            spimi_index.update({term: postings_list})
    return spimi_index

class QueryHandler:
    """Handles boolean retrieval queries"""
    def __init__(self):
        self.spimi_index = read_spimi_index()
        self.terms = []

    def execute(self, queryInput):
        """Execute query"""
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
            return 0

        # Extract terms and apply same preprocessing used for creating the SPIMI index
        query_terms = queryInput.strip().replace(" ", "").split(seperator)
        self.terms = normalize(query_terms)

        # Collect postings lists of query terms
        tpl = []
        for term in self.terms:
            if term in self.spimi_index:
                tpl.append(self.spimi_index[term])

        if query_type == 'AND':
            query_result = set(tpl[0]).intersection(*tpl)
        else:
            query_result = []
        return list(query_result)

if __name__ == '__main__':
    query()
