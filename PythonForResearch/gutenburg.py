from collections import Counter
import pandas as pd


def count_words(text):
    text = text.lower()
    puncuation = ['.', ',', '?', '!', "'", '"']
    for char in puncuation:
        text = text.replace(char, '')
    print(text)

    word_counts = Counter(text.split(' '))
    return word_counts


def read_book(title_path):
    with open(title_path, 'r', encoding='utf8') as f:
        text = f.read()
        text = text.replace('/n', '').replace('/r', '')
        return text


def word_stats(word_counts):
    num_unique = len(word_counts)
    counts = word_counts.values()
    return num_unique, counts


test = "Vamsi is a loser because he doesn't wear pants Vamsi"
print(read_book('Books_EngFr/Books_EngFr/English/shakespeare/Romeo and Juliet.txt'))
