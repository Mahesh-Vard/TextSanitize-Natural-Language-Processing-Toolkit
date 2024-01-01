import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')
import re
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import wordnet
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from bs4 import BeautifulSoup

def cleanText(text, lemmatize=True, stemmer=True, remove_stopwords=True):
    """Method for cleaning text from train and test data. Removes numbers, punctuation, and capitalization. Stems or lemmatizes text."""
    
    if isinstance(text, float):
        text = str(text)
    if isinstance(text, np.int64):
        text = str(text)
    try:
        text = text.decode()
    except AttributeError:
        pass

    # Removing HTML tags
    soup = BeautifulSoup(text, "lxml")
    text = soup.get_text()

    # Removing non-alphabetic characters
    text = re.sub(r"[^A-Za-z]", " ", text)

    # Converting to lowercase
    text = text.lower()

    if remove_stopwords:
        stop_words = set(stopwords.words("english"))
        text = " ".join([word for word in text.split() if word not in stop_words])

    if lemmatize:
        wordnet_lemmatizer = WordNetLemmatizer()

        def get_tag(tag):
            if tag.startswith('J'):
                return wordnet.ADJ
            elif tag.startswith('V'):
                return wordnet.VERB
            elif tag.startswith('N'):
                return wordnet.NOUN
            elif tag.startswith('R'):
                return wordnet.ADV
            else:
                return ''

        tokens = word_tokenize(text)
        tagged = pos_tag(tokens)
        text = " ".join([wordnet_lemmatizer.lemmatize(t[0], get_tag(t[1][:2])) if get_tag(t[1][:2]) else wordnet_lemmatizer.lemmatize(t[0]) for t in tagged])

    if stemmer:
        snowball_stemmer = SnowballStemmer('english')
        text = " ".join([snowball_stemmer.stem(t) for t in word_tokenize(text)])

    return text

# Example usage:
text = input("Enter text: ")
cleaned_text = cleanText(text, lemmatize=True, stemmer=True, remove_stopwords=True)
print("Cleaned Text:", cleaned_text)
    
