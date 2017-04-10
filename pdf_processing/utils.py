# utils.py
# -*- coding: utf-8 -*-
# @Author: Sidharth Mishra and Michael Symonds
# @Date:   2017-04-03 19:45:31
# @Last Modified by:   Michael Symonds
# @Last Modified time: 2017-04-09 20:51:26




'''
Some Utilities and Stemming algorithms
'''


# Python standard library imports

# Pypi
from stemming.porter2 import stem
from nltk.corpus import stopwords


def standardize_words(words):
  '''
  Takes the list of words it needs to standardize and then returns a list of standardized words.
  The list of standardized words contains only single words, all phrases are removed so goes for
  empty strings.

  :param words: The list of words that needs to be standardized. :class: `list(str)`

  :return: standardized_words :class: `list(str)`
  '''
  
  stops = set(stopwords.words("english"))
  symbols = {'.', ',', ';', '/', ':', '\\', '-', '(', ')', '&', '@', '!', '#', '$', '%', '^', '*', '\''
             , u"\u0022", u"\u0027", u"\u02ba", u"\u02dd", u"\u02ee", u"\u02f6", u"\u05f2", u"\u05f4"
             , u"\u1cd3", u"\u201c", u"\u201d", u"\u201f", u"\u2033", u"\u2036", u"\u3003", u"\uff02"
             , u"\u2019"}
  
  standardized_words = []
  result = []
  for word in words:
    if ' ' in word:
      word_splits = list(filter(lambda x: len(x) > 0, word.strip(' ').split(' ')))
      standardized_words.extend(word_splits)
    elif word != '' or len(word) != 0:
      standardized_words.append(word)

  for word in standardized_words:
    while len(word) > 0 and word[len(word) - 1] in symbols:
      word = word[:-1]
    while len(word) > 0 and word[0] in symbols:
      word = word[1:]
    if not any(char in symbols or char.isdigit() for char in word):
      if len(word) > 0 and word.lower() not in stops and word != u"\u00A9":
        result.append(stem(word))

  return result




if __name__ == '__main__':
  # do nothing
  pass
