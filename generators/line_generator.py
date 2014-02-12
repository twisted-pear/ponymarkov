#!/usr/bin/env python2

import nltk
from nltk.probability import LidstoneProbDist

import re

import generator

class LineGenerator(generator.GeneratorI):
    def __init__(self, provider):
        lines = provider.get_lines()

        if not lines:
            raise Exception("Provider returned no lines.")

        tokenizer = nltk.tokenize.RegexpTokenizer(r'[\S]+')
        tokenized_lines = tokenizer.tokenize(' '.join(lines))

        estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
        self.__model = nltk.NgramModel(3, tokenized_lines, estimator)

    def generate(self, min_words = 10):
        starting_words = self.__model.generate(100)[-2:]
        while starting_words[0][0].islower():
            starting_words = self.__model.generate(1, starting_words)[-2:]

        min_words = max(min_words - 2, 1)

        words = self.__model.generate(min_words, starting_words)
        while not re.match(r'[\S]+[.!?]$', words[-1]):
            words.append(self.__model.choose_random_word(words))

        return words
