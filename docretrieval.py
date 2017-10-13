import ast

from collections import OrderedDict

def query():
    """ """
    query = QueryHandler()
    user_input = input("Enter your boolean query using && or || exclusively:")
    print("Executing: " + user_input + "...")
    result = query.execute(user_input)

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
    """Handle boolean retrieval queries"""
    def __init__(self):
        self.spimi_index = read_spimi_index()

    def execute(self, query):
        """Execute query"""
        self.parseQuery(query)
        print("Boolean retrieval complete!")

    def parseQuery(self, queryInput):
        """Validate and parse query"""
        and_index = queryInput.index('&&') if '&&' in queryInput else -1
        or_index = queryInput.index('||') if '||' in queryInput else -1
        if (and_index > 0) and (or_index < 0):
            print("AND query")
            query_type = 'AND'
        elif (or_index > 0) and (and_index < 0):
            print('OR query')
            query_type = 'OR'
        else:
            print('Invalid query')
            return 0

        test = queryInput.split(' || ')
        print(test, query_type)

if __name__ == '__main__':
    query()
