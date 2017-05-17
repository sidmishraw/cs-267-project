# process_results.py
# -*- coding: utf-8 -*-
# @Author: Sidharth Mishra
# @Date:   2017-05-17 14:42:23
# @Last Modified by:   Sidharth Mishra
# @Last Modified time: 2017-05-17 16:49:27

"""
Processes the results.txt obtained by running either Simplicial Complex C++ program or the
Apriori C++ port and uses the word_map.json file to obtain the words from their respective indices.
"""

# pystdlib imports~
from re import compile
from re import findall
from json import loads
from json import dumps
from json import load
from json import dump

# chardet ~
from chardet import detect

# simplex dictionary, the final word mapping
simplex_dict = {}
num_word_map = {}
docs_map = {}
__FINAL_SIMPL_CMPLX__ = "final_simplicialcmplx_results.json"
__FINAL_AP__ = "final_apriori_results.txt"


def split_replace_simplex(x, simplex_l, num_word_map):
  simplex_l.append(num_word_map[x])


def process_results_txt_simplicial_complex(num_word_map, docs_map):
  """
  Processes the results.txt obtained from Simplicial Complex C++ program to obtain
  `final_simplicialcmplx_results.txt` replacing all the numbers with the words from the
  number - word mapping while constructing the .dat file.
  """

  pattern = compile(r'\[(.*)\]\s(\d*)')

  with open('results.txt', 'r') as fin:
    for s_in in fin:
      # print(s_in)
      if len(findall(pattern, s_in)) > 0:
        simplex, freq = findall(pattern, s_in)[0]
        simplex_l = []
        list(
            map(
                lambda x: split_replace_simplex(
                    x,
                    simplex_l,
                    num_word_map),
                simplex.strip(" ").split(' ')))
        new_simplex = '[{}]'.format(' '.join(simplex_l))
        simplex_dict[new_simplex] = int(freq)


def process_results_txt_apriori(num_word_map, docs_map):
  """
  Processes the results.txt obtained from Simplicial Complex C++ program to obtain
  `final_simplicialcmplx_results.txt` replacing all the numbers with the words from the
  number - word mapping while constructing the .dat file.
  """

  pattern = compile(r'\[\[(.*)\]\]\s(\d*)')

  with open('results.txt', 'r') as fin:
    for s_in in fin:
      if len(findall(pattern, s_in)) > 0:
        simplex, freq = findall(pattern, s_in)[0]
        # print("{s} : {f}".format(s=simplex, f=freq))
        simplex_l = []
        list(
            map(
                lambda x: split_replace_simplex(
                    x,
                    simplex_l,
                    num_word_map),
                simplex.strip(" ").split(' ')))
        new_simplex = '[{}]'.format(' '.join(simplex_l))
        simplex_dict[new_simplex] = int(freq)


if __name__ == '__main__':
  print("""
    ------------------------------------------------------
    ------------------ RESULT PROCESSOR ------------------
    ------------------------------------------------------
    """)
  print("Detecting encoding of the files word_map.json and doc_map.json:")
  with open("word_map.json", "rb") as wordmap_f:
    s = wordmap_f.read()
    chardet_detected_encoding = detect(s)['encoding']
    print(
        'Character Encoding detected for word_map.json = ',
        chardet_detected_encoding)
    num_word_map = loads(str(s, encoding=chardet_detected_encoding))

  with open("doc_map.json", "rb") as docmap_f:
    s = docmap_f.read()
    chardet_detected_encoding = detect(s)['encoding']
    print(
        'Character Encoding detected for doc_map.json = ',
        chardet_detected_encoding)
    docs_map = loads(str(s, encoding=chardet_detected_encoding))

  print("Which results.txt file are you processing?")
  print("Press: ")
  print("0: Simplicial Complex, or")
  print("1: Apriori C++ port")

  x = int(input("Enter your option:"))

  if x == 0:
    process_results_txt_simplicial_complex(num_word_map, docs_map)
    with open(__FINAL_SIMPL_CMPLX__, 'w') as fopen:
      fopen.write(dumps(simplex_dict))
    print(
        "Generated the file: {filename}".format(
            filename=__FINAL_SIMPL_CMPLX__))
    exit(0)
  elif x == 1:
    process_results_txt_apriori(num_word_map, docs_map)
    with open(__FINAL_AP__, 'w') as fopen:
      fopen.write(dumps(simplex_dict))
    print("Generated the file: {filename}".format(filename=__FINAL_AP__))
    exit(0)
  else:
    print("0 or 1 only please!")
    exit(0)
