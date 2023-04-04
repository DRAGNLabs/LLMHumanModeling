import re
import string
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk import download as nltk_download

nltk_download('punkt')
nltk_download('wordnet')

# NLTKs English stop words:
# https://gist.github.com/sebleier/554280#:~:text=%5B%22i%22%2C%20%22me%22%2C%20%22my,don%22%2C%20%22should%22%2C%20%22now%22%5D

STOPWORDS = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
STOPWORDS += "wikipedia"  # Appears in every search
STOPWORDS += ["#", "&", "|", "!", "(", ")", "-", "[", "]", "{", "}", ";", "*", ":", "\\", ",", "<", ">", ".", "\/", "?", "@", "_", "~"]  # What about '%' nd '$'??

# PUNCTUATION = re.compile('[%s]' % re.escape(string.punctuation))
# STEMMER = Stemmer.Stemmer('english')

def lowercase_filter(tokens):
    return [token.lower() for token in tokens]

def tokenize(text: str)-> list[str]:
    return word_tokenize(text) # text.split()  # he had a white-sace tokenizer that I found to be weak

# def punctuation_filter(tokens):
#     return [PUNCTUATION.sub('', token) for token in tokens]

def stopword_filter(tokens: list[str])-> list[str]:
    return [token for token in tokens if token not in STOPWORDS]

# def stem_filter(tokens):   # replaced with lemmatizer
#     return STEMMER.stemWords(tokens)

def lemma_filter(tokens: list[str])-> WordNetLemmatizer:
    lemmatizer = WordNetLemmatizer()
    return lemmatizer.lemmatize(tokens)

def analyze_(text:str)-> list[str]:
    tokens = tokenize(text)
    tokens = lowercase_filter(tokens)
    # tokens = punctuation_filter(tokens)
    tokens = stopword_filter(tokens)
    # tokens = stem_filter(tokens)
    tokens = [lemma_filter(token) for token in tokens]

    return [token for token in tokens if token]