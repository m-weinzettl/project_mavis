import json
import numpy as np
import pickle
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from nltk_utils import tokenize, stem, bag_of_words

with open('packages/data/intents.json', 'r', encoding='utf-8') as f:
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

input_size = len(all_words)
hidden_size = 8
output_size = len(tags)

model = Sequential([
    # LAYER 1 & 2: Eingangsschicht (input_shape) + Erste versteckte Schicht (Dense mit 8 Neuronen)
    Dense(hidden_size, input_shape=(input_size,), activation='relu'),

    # LAYER 3: Erste Ausblendschicht (Dropout schaltet zufällig 20% der Neuronen ab)
    Dropout(0.2),

    # LAYER 4: Zweite versteckte Schicht (Dense mit 8 Neuronen)
    Dense(hidden_size, activation='relu'),

    # LAYER 5: Zweite Ausblendschicht (Dropout schaltet zufällig 20% der Neuronen ab)
    Dropout(0.2),

    # LAYER 6: Ausgangsschicht (Output-Größe entspricht der Anzahl deiner Kategorien/Tags)
    Dense(output_size, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

print("--- Training gestartet ---")
model.fit(X_train, y_train, epochs=1000, batch_size=8, verbose=1)
print("--- Training erfolgreich beendet ---")

model.save('model/mavis_model.keras')

data = {
    "all_words": all_words,
    "tags": tags
}

with open("packages/model/training_data.pkl", "wb") as f:
    pickle.dump(data, f)

print("KI-Gehirn erfolgreich unter 'model/' archiviert!")