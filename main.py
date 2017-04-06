# main.py
# -*- coding: utf-8 -*-
# @Author: Samuel Ordonia
# @Date:   2017-04-04 18:32:49
# @Last Modified by:   Sidharth Mishra
# @Last Modified time: 2017-04-05 23:14:43




"""
The main driver for CS 267 Project.
"""




# Python Standard library imports
from re import sub
from json import dumps
from json import loads
from os.path import sep




# Numpy
import numpy as np
import pandas as pd




# CS 267 Project imports
from apriori import *
from simplicial_complex import SimplicialComplex




# globals
corpus = None
tokens = None
token_list = None
docs = None
df_output = None
props = None




# constants
__INPUT_FILEPATH__ = 'input_jsons_filepath'
__SHARED_OBJ_FILEPATH__ = 'shared_obj_filepath'
__OUTPUT_FILEPATH__ = 'output_filepath'




# read in data and init
def read_data_init():
    '''
    Reads in data and initializes the pipeline.

    :return: `None`
    '''

    global corpus, token_list, docs, props

    with open('properties.json', 'r') as props_read:
        props = loads(props_read.read())

    (corpus, tokens) = read_input_files(props[__INPUT_FILEPATH__])
    token_list = list(tokens.keys())

    docs = sorted(corpus.keys())




# Part1 section: tf - compute term frequencies
def get_term_frequency():
    '''
    Compute the term frequencies.

    :return: `None`
    '''

    global docs, props

    term_frequency_with_positions = dict()

    for doc in docs:
        term_frequency_with_positions[doc] = determine_word_positions(corpus[doc])

    # Print to json file & prettify
    with open('{filepath}{sep}output_term_freq.json'.format(\
        filepath = props[__OUTPUT_FILEPATH__], sep = sep), 'w') as tf_file_output:
    
        tf_file_output.write(dumps(term_frequency_with_positions, sort_keys=True, indent=2))




# compute document frequency
def compute_df():
    '''
    Computes the df.
    '''

    global docs, token_list, corpus, props, df_output

    # Part 2 section:  df
    df_output = determine_doc_frequency(docs, token_list, corpus)

    # Print to csv file
    df_output.to_csv('{filepath}{sep}output_doc_freq.csv'.format(\
        filepath = props[__OUTPUT_FILEPATH__], sep = sep), header=token_list, sep=',')

    # Print to txt file
    np.savetxt('{filepath}{sep}output_doc_freq.txt'.format(\
        filepath = props[__OUTPUT_FILEPATH__], sep = sep), df_output.values, fmt='%d')




# simplical complex
def process_simplical_cmplx():
    '''
    Use Simplical Complex algorithm to find frequent itemset.

    :return: `None`
    '''

    global df_output, props

    string_vector_all = ''

    for index, series in df_output.iterrows():
        whitespace_regex = r'\s+'
        string_vector = np.array_str(series.values)
        string_vector = sub(whitespace_regex, '', string_vector)
        string_vector_all += string_vector_all + string_vector[1:len(token_list)]
        bit_vector_as_string = string_vector[1:(len(token_list))].encode('utf-8')

    bit_vector_as_string = string_vector_all.encode('utf-8')
    sc2 = SimplicialComplex(shared_obj_path = props[__SHARED_OBJ_FILEPATH__])
    sc2.directProcess(1, 0.05, len(token_list) - 1, len(docs), bit_vector_as_string)




if __name__ == '__main__':
    read_data_init()
    get_term_frequency()
    compute_df()
    process_simplical_cmplx()
