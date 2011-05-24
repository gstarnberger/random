#!/usr/bin/env python

# Simple spellchecker
# Guenther Starnberger <guenther@starnberger.name>

from __future__ import with_statement

import sys
import itertools
import difflib

# Monkey patch itertools if installed version does not include izip_longest
if sys.version_info < (2, 6, 0):
    from izip_longest import izip_longest
    itertools.izip_longest = izip_longest


# FIXME: The way how I interpret the specification the checker should only fix
# 'repeated characters', but not 'missing characters' when the same character
# is repeated multiple times in the correct version of the word. Therefore,
# e.g., 'tree' or 'true' are no valid spelling suggestions for the input 'tre'.
# This makes the whole code a little bit more complicated, as the normalized
# representation of both cases would be the same. If 'tree' should be a valid
# spelling suggestion for 'tre', the check_repetition() function can be
# removed.

# FIXME: This program does not put any assumptions on the character set of the
# input. In a 'real world' application the input must be correctly decoded if
# another charset than US-ASCII is used. For example, if the input is UTF-8
# encoded Unicode, Python's string.decode method can be used to decode the
# UTF-8 encoding into a Unicode Python string.


# Runtime complexity:
# -------------------
#
# A worst case occurs if all the words in the wordlist normalize to the same
# value. In that case the complexity would be
#
# O(words_in_wordlist) + O(words_in_wordlist * log(words_in_wordlist) *
# words_in_checked_input)
#
# as Python's difflib.get_close_matches() would need to analyze each single
# word in the word list in order to find the best match. For this case I assume
# that the complexity of Python's difflib.get_close_matches() is O(n * log n),
# as this function is using a heapq internally to sort the results.
#
# However, when we only want to return _any_ valid result (as allowed by the
# spec) instead of the best valid result, we can decrease the runtime
# complexity to
#
# O(words_in_wordlist) + O(words_in_checked_input)
#
# by only returning the first result that normalizes to a given value.
#
# Remark 1: For the analysis above I assumed that checking each individual word
# has a linear worst-case, which can, e.g., be the case when we restrict the
# maximal allowed length of each word to a fixed value. If there is no limit,
# for each iteration over the wordlist and/or the input to be checked we would
# therefore also need to take the length of the respective word into account
# (basically multiplying the current complexity by the word length).
#
# Remark 2: The analysis above reflects the complexity for the average cases.
# If we look at worst-case conditions the runtime of Python's data structures
# can seriously degrade, compared to the average runtime. For example, this
# would be the case if there occur are a lot of internal collisions in the
# Python dictionary and the set used to store the wordlist. Instead of having
# the expected constant lookup time of the dictionary, the performance would
# degrade to a linear runtime. As those functions are called in each single
# iteration, the total runtime would be something like (if we return the first
# result instead of the best result):
#
# O(words_in_wordlist^2) + O(words_in_checked_input * words_in_wordlist)
#
# See http://wiki.python.org/moin/TimeComplexity for the time complexity of
# Python's internal functions.


def get_content(filename):
    '''Open the given file and yield the individual words, allowing the caller
    to iterate over the input.'''

    with open(filename) as f:
        for line in f:
            for word in line.split():
                yield word


def normalize(word, handle_duplicates=True):
    '''Normalize a given word according to the rules defined in the
    specification on http://www.justin.tv/problems/spellcheck. The normalized
    version of a misspelled word will always be equal to the normalized version
    of the respective correct word.'''

    def lowercase(word):
        return word.lower()

    def normalize_vowels(word):
        vowels = ['a', 'e', 'i', 'o', 'u']
        return ''.join([vowels[0] if x in vowels else x for x in word])

    def remove_duplicates(word):
        return ''.join([x for (x, y) in itertools.izip_longest(word, word[1:]) if x != y])

    # The order of the called functions is important, e.g., before removing the
    # duplicates we need to normalize the case and the vowels.
    normalize_funcs = [lowercase, normalize_vowels]

    if handle_duplicates:
        normalize_funcs.append(remove_duplicates)

    for function in normalize_funcs:
        word = function(word)

    return word


def check_repetition(input_word, correct_word):
    '''This function is required in order to guarantee the correct behavior in
    case of repetition. According to the specification only repeated characters
    in the input should be corrected, but not missing characters of sequences
    with repeated characters. E.g., if the input is 'tre' the words 'true' or
    'tree' must be a valid spelling suggestion. However, due to the way how the
    normalization function works those words would be treated as valid spelling
    suggestion. Therefore, this function can be used to validate if a
    suggestion is valid, before it is returned to the user.'''

    input_list = []
    correct_list = []

    for word, check_list in [(input_word, input_list), (correct_word, correct_list)]:
        for _, group in itertools.groupby(word):
            check_list.append(list(group))

    for x, y in itertools.izip_longest(input_list, correct_list):
        if x is None or y is None:
            return False

        if x[0] != y[0]:
            return False

        if len(list(x)) < len(list(y)):
            return False

    return True


def spellcheck(wordlist_name):
    '''The main spellcheck function. First iterate over the wordlist and store a
    hash of the normalized words. Afterwards, read the user input, check if we
    find a matching normalized word, and return the best matching result.'''

    normalized_mapping = {}
    plain_wordlist = set()

    for word in get_content(wordlist_name):
        plain_wordlist.add(word)
        normalized_word = normalize(word)

        if normalized_word in normalized_mapping:
            normalized_mapping[normalized_word].add(word)
        else:
            word_set = set()
            word_set.add(word)
            normalized_mapping[normalized_word] = word_set

    while True:
        try:
            input_word = raw_input('> ')
        except EOFError:
            break

        if input_word in plain_wordlist:
            print input_word
        else:
            normalized_word = normalize(input_word)
            if normalized_word in normalized_mapping:
                candidates = itertools.ifilter(lambda x: check_repetition(normalize(input_word, False), normalize(x, False)),
                                               normalized_mapping[normalized_word])
                suggestions = difflib.get_close_matches(input_word, candidates, 1, 0)
                if len(suggestions) > 0:
                    print suggestions[0]
                    continue

            print 'NO SUGGESTION'


if __name__ == '__main__':
    spellcheck(sys.argv[1] if len(sys.argv) >= 2 else '/usr/share/dict/words')
