import json
import random
import os
import speech_recognition as sr
import pyttsx3
import numpy as np
import pickle
import tensorflow as tf
from nltk_utils import tokenize, stem, bag_of_words

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = False
    recognizer.energy_threshold = 300
