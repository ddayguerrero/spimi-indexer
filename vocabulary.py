import nltk
from nltk.corpus import stopwords
import string

def preprocess(documents):
    """ Tokenize and normalize documents """
    # nltk.download('stopwords')
    # print(" Fetching stopwords...")
    # stops = list(set(stopwords.words("english")))
    # stops_30 = stops[:30]
    # stops_150 = stops[:150]
    print(" -- Tokenizing...")
    print(" -- Normalizing...")
    print(" --- 1- Tokens with punctuation characters...")
    print(" --- 2- Tokens with blank or empty strings...")
    print(" --- 3- Tokens with unprocessed encoding...")
    print(" --- 4- Lowercase...")
    print(" --- 5- Tokens with digits or numbers...")
    for key in documents:
        # Tokenize (case folding is automatically applied within the built-in function)
        tokens = nltk.word_tokenize(str(documents[key]))
        # Normalize
        processed_tokens = tokens
        # Design decision: discard tokens with punctuation marks
        processed_tokens = [token for token in processed_tokens if not token in string.punctuation]
        # Design decision: discard blank and empty strings tokens
        processed_tokens = filter(None, processed_tokens)
        processed_tokens = [token for token in processed_tokens if not token == "''" and not token == '``']
        # Design decision: discard tokens with unwanted encoding
        processed_tokens = [token for token in processed_tokens if not token == "\x03" and not token == "\x7f"]
        # Apply lowercase
        processed_tokens = [i.lower() for i in processed_tokens]
        # Discard token if a containing character is a digit
        processed_tokens = [token for token in processed_tokens if not any(char.isdigit() for char in token)]
        # Discard token if it is a English language stopword - 30 terms
        # print(" --- 6- Removing 30 stop words...")
        # processed_tokens = [token for token in processed_tokens if not token in stops_30]
        # Discard token if it is a English language stopword - 150 terms
        # print(" --- 7- Removing 150 stop words...")
        # processed_tokens = [token for token in processed_tokens if not token in stops_150]
        # print(" --- 8- Applying Porter Stemmer...")
        # print(processed_tokens)
        documents[key] = processed_tokens
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
    # Design decision: discard tokens with unwanted encoding
    processed_tokens = [token for token in processed_tokens if not token == "\x03" and not token == "\x7f"]
    # Apply lowercase
    processed_tokens = [i.lower() for i in processed_tokens]
    # Discard token if a containing character is a digit
    processed_tokens = [token for token in processed_tokens if not any(char.isdigit() for char in token)]
    return processed_tokens
