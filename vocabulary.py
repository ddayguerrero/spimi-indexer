import nltk
from nltk.corpus import stopwords
import string
import ast

def preprocess(documents):
    """ Tokenize and normalize documents """
    # nltk.download('stopwords')
    print("Fetching stopwords...")
    # stops = list(set(stopwords.words("english")))
    # stops_30 = stops[:30]
    # stops_150 = stops[:150]
    print(" -- Tokenizing...")
    print(" -- Normalizing...")
    print(" --- 1- Tokens with punctuation characters...")
    print(" --- 2- Tokens with blank or empty strings...")
    print(" --- 3- Tokens with invalid code points from encoding...")
    print(" --- 4- Tokens with digits or numbers...")
    print(" --- 5- Lowercase...")
    # print(" --- 6- 30 English stop words...")
    # print(" --- 5- 150 English stop words...")
    for key in documents:
        # Tokenize (case folding is automatically applied within the built-in function)
        tokens = nltk.word_tokenize(str(documents[key]))
        # processed_tokens = normalize(tokens, stops_30, stops_150)
        processed_tokens = normalize(tokens)
        documents[key] = processed_tokens
        #documents[key] = tokens

    non_positional_postings_count = 1
    for index, val in enumerate(documents):
        non_positional_postings_count += len(documents[val])
    print("Tokens - Number of positions entries in postings: ", non_positional_postings_count)
    print("Preprocessing Complete!")
    return documents

def normalize(tokens):
    # Normalize
    processed_tokens = tokens
    # Design decision: discard tokens with punctuation marks
    processed_tokens = [token for token in processed_tokens if not token in string.punctuation]
    # Design decision: discard blank and empty strings tokens
    processed_tokens = filter(None, processed_tokens)
    processed_tokens = [token for token in processed_tokens if not token == "''" and not token == '``']
    # Design decision: discard tokens with invalid code points from UTF-8 encoding
    processed_tokens = [token for token in processed_tokens if not token == "\x03" and not token == "\x7f"]
    # Discard token if a containing character is a digit
    # processed_tokens = [token for token in processed_tokens if not any(char.isdigit() for char in token)]
    # Discard token if it is convertable to a number (int or float)
    processed_tokens = [token for token in processed_tokens if not is_number(token)]
    # Apply lowercase
    processed_tokens = [token.lower() for token in processed_tokens]
    # Discard token if it is a English language stopword - 30 terms
    # processed_tokens = [token for token in processed_tokens if not token in stops_30]
    # Discard token if it is a English language stopword - 150 terms
    # processed_tokens = [token for token in processed_tokens if not token in stops_150]
    # print(" --- 8- Applying Porter Stemmer...")
    # print(processed_tokens)
    return processed_tokens

def is_number(value):
    try:
        number = ast.literal_eval(value)
        if isinstance(number, int) or isinstance(number, float):
            return True
        else:
            return False
    except:
        return False
