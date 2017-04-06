# utils.py
# -*- coding: utf-8 -*-
# @Author: Sidharth Mishra
# @Date:   2017-04-03 19:45:31
# @Last Modified by:   Sidharth Mishra
# @Last Modified time: 2017-04-05 20:33:26




'''
Some Utilities and Stemming algorithms
'''


# Python standard library imports




def standardize_words(words):
  '''
  Takes the list of words it needs to standardize and then returns a list of standardized words.
  The list of standardized words contains only single words, all phrases are removed so goes for
  empty strings.

  :param words: The list of words that needs to be standardized. :class: `list(str)`

  :return: standardized_words :class: `list(str)`
  '''

  standardized_words = []

  for word in words:
    if ' ' in word:
      word_splits = list(filter(lambda x: len(x) > 0, word.strip(' ').split(' ')))
      standardized_words.extend(word_splits)
    elif word != '' or len(word) != 0:
      standardized_words.append(word)

  return standardized_words




if __name__ == '__main__':
  # do nothing
  pass
