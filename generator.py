#!/usr/bin/env python2

import cPickle as pickle

class GeneratorI:
    def generate(self, min_words = 0):
        raise NotImplementedError("Please implement this yourself.")

    @staticmethod
    def load(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)
