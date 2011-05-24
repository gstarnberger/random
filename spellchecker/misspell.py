#!/usr/bin/env python

# Generate words with spelling errors
# Guenther Starnberger <guenther@starnberger.name>

from __future__ import with_statement

import sys
import random


def get_content(filename):
    '''Open the given file and yield the individual words, allowing the caller
    to iterate over the input.'''

    with open(filename) as f:
        for line in f:
            for word in line.split():
                yield word


def misspell(wordlist_name):
    '''Misspells a wordlist according to the rules on
    http://www.justin.tv/problems/spellcheck.'''

    def repeat_characters(word):
        return ''.join(map(lambda x: x * random.randint(1, 3), word))

    def lowercase(word):
        return ''.join(map(lambda x: x.upper() if random.choice([True, False]) else x.lower(), word))

    def mix_vowels(word):
        vowels = ['a', 'e', 'i', 'o', 'u']
        return ''.join(map(lambda x: random.choice(vowels) if x in vowels else x, word))

    # The order of the called functions is important: First repeat the
    # characters, so that the case randomization and the vowel mixing can be
    # executed on the repeated characters.
    misspell_funcs = [repeat_characters, lowercase, mix_vowels]

    for word in get_content(wordlist_name):
        for function in misspell_funcs:
            word = function(word)

        print word


if __name__ == '__main__':
    misspell(sys.argv[1] if len(sys.argv) >= 2 else '/usr/share/dict/words')
