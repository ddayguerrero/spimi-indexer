import nltk
from nltk.corpus import stopwords
import string

def preprocess(documents):
    """ Tokenize and normalize documents """
    print(" - Preprocessing documents...")
    nltk.download('stopwords')
    stops = list(set(stopwords.words("english")))
    stops_30 = stops[:30]
    stops_150 = stops[:150]
    for key in documents:
        # Tokenize (case folding is automatically applied within the built-in function)
        print(" -- Tokenizing...")
        tokens = nltk.word_tokenize(str(documents[key]))
        # Normalize
        print(" -- Normalizing...")
        processed_tokens = tokens
        # Design decision: remove punctuation marks
        print(" --- 1- Remove punctuation characters...")
        processed_tokens = [token for token in processed_tokens if not token in string.punctuation]
        # Map .lower() to each token
        print(" --- 2- Applying lower case...")
        processed_tokens = [i.lower() for i in processed_tokens]
        # Discard token if a containing character is a digit
        print(" --- 3- Removing numbers...")
        processed_tokens = [token for token in processed_tokens if not any(char.isdigit() for char in token)]
        # Discard token if it is a English language stopword
        print(" --- 4- Removing 30 stop words...")
        processed_tokens = [token for token in processed_tokens if not token in stops_30]
        print(" --- 5- Removing 150 stop words...")
        processed_tokens = [token for token in processed_tokens if not token in stops_150]
        print(" --- 6- Applying Porter Stemmer...")
        print(processed_tokens)
    print("=== Preprocessing Complete ===")
