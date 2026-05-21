import json
import numpy as np
import pickle
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from nltk_utils import tokenize, stem, bag_of_words

# 1. Datensätze aus der professionellen Ordnerstruktur laden
with open('data/intents.json', 'r', encoding='utf-8') as f:
    intents = json.load(f)

all_words = []
tags = []
xy = []

for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        w = tokenize(pattern)
        all_words.extend(w)
        xy.append((w, tag))

ignore_words = ['?', '!', '.', ',']
all_words = [stem(w) for w in all_words if w not in ignore_words]
all_words = sorted(list(set(all_words)))
tags = sorted(list(set(tags)))

X_train = []
y_train = []

for (pattern_sentence, tag) in xy:
    bag = bag_of_words(pattern_sentence, all_words)
    X_train.append(bag)
    label = tags.index(tag)
    y_train.append(label)

X_train = np.array(X_train)
y_train = np.array(y_train)

# 2. Parameter für das neuronale Netz definieren
input_size = len(all_words)
hidden_size = 8
output_size = len(tags)

# 3. Das neuronale Netz erstellen (Sequential Model)
model = Sequential([
    Dense(hidden_size, input_shape=(input_size,), activation='relu'),
    Dropout(0.2),  # Verhindert Overfitting (Überanpassung)
    Dense(hidden_size, activation='relu'),
    Dropout(0.2),
    Dense(output_size, activation='softmax')  # Liefert Wahrscheinlichkeiten für die Tags
])

# Modell kompilieren
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

print("--- Training gestartet ---")
# 4. Modell trainieren
model.fit(X_train, y_train, epochs=200, batch_size=8, verbose=1)
print("--- Training erfolgreich beendet ---")

# 5. Modell und Metadaten im 'model/'-Ordner speichern
model.save('model/mavis_model.h5')

# Wichtige Zusatzdaten speichern, damit die Live-Erkennung die exakten Dimensionen kennt
data = {
    "all_words": all_words,
    "tags": tags
}

with open("model/training_data.pkl", "wb") as f:
    pickle.dump(data, f)

print("KI-Gehirn erfolgreich unter 'model/' archiviert!")