import json
import nltk
from nltk.stem.snowball import SnowballStemmer

# Lädt die benötigten Punkt-Daten für die Wort-Trennung herunter
nltk.download('punkt', quiet=True)

# Wir nutzen den deutschen Stemmer für professionelle Wortstamm-Reduktion
stemmer = SnowballStemmer("german")


def tokenize(sentence):
    """Zerlegt einen Satz in einzelne Wörter (z.B. 'Hallo Mavis' -> ['Hallo', 'Mavis'])"""
    return nltk.word_tokenize(sentence, language='german')


def stem(word):
    """Kürzt ein Wort auf seinen Stamm (z.B. 'öffnen', 'öffne', 'öffnet' -> 'öffn')"""
    return stemmer.stem(word.lower())


def bag_of_words(tokenized_sentence, all_words):
    """
    Erstellt einen Zahlen-Vektor (0 oder 1) für TensorFlow.
    Für jedes Wort im Satz, das in 'all_words' existiert, wird eine 1 gesetzt.
    """
    tokenized_sentence = [stem(w) for w in tokenized_sentence]
    bag = [0] * len(all_words)

    for idx, w in enumerate(all_words):
        if w in tokenized_sentence:
            bag[idx] = 1

    return bag