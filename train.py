import json
import numpy as np
from nltk_utils import tokenize, stem, bag_of_words


with open ("data/intents.json", "r") as read_file:
    intents = json.load(read_file)

all_words = []
tags = []
xy = []

for intent in intents["intents"]:
    tag = intent["tag"]
    tags.append(tag)
    for pattern in intent["patterns"]:
        # satz in wort zerlegen
        w = tokenize(pattern)
        all_words.append(w)
        # wort satz paar in xy speichern
        xy.append(w)

ignore_words = ['?', '!','.', ',']
all_words = [stem(w) for w in all_words if w not in ignore_words]
# duplicates enfernen
all_words = sorted(list(set(all_words)))
tags = sorted(list(set(tags)))

print(f"{len(xy)} Muster (Patterns) gefunden.")
print(f"{len(tags)} Kategorien (Tags) gefunden: {tags}")
print(f"{len(all_words)} einzigartige Wörter (nach Stemming) extrahiert.\n")

x_train = []
y_train = []

for(pattern_sentence, tag) in xy:
    bag = bag_of_words(pattern_sentence, all_words)
    x_train.append(bag)

    label = tags.index(tag)
    y_train.append(label)

x_train = np.array(x_train)
y_train = np.array(y_train)

print("--- Daten-Preprocessing erfolgreich! ---")
print(f"Form der Eingangsdaten (X_train): {x_train.shape}")
print(f"Form der Ausgangsdaten (y_train): {y_train.shape}")