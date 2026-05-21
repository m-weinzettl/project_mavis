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
