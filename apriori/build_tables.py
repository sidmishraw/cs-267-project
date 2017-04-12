# build_tables.py
# -*- coding: utf-8 -*-
# @Author: Samuel Ordonia | sordonia120446 | Sam O
# @Date:   2017-04-05 20:25:02
# @Last Modified by:   Sidharth Mishra
# @Last Modified time: 2017-04-05 22:59:58




"""
Builds the following tables:
    1) (Dict) Alphabetically ordered words for each document and their positions.
    2) (Bit-Matrix) Alphabetically ordered words across all documents and which
    documents each occurs in.

Created on 2/25/2017

@author: sordonia120446 | Sam O
"""




import os, re, json
from collections import defaultdict
from collections import OrderedDict
import numpy as np
import pandas as pd




def read_input_files(filepath):
    """
    Input is the filepath to all files.
    Steps for text files:
        Goes through each file.
        Extracts text.
        Removes regex's.
        Lower-cases all leters.
    Steps for json files:
        Goes through each page's array of page_content.
    Returns a filename-[words] key-value pair dict and an OrderedDict of token-doc.
    """
    corpus = dict()
    tokens = OrderedDict(docs=os.listdir(filepath))
    for file in os.listdir(filepath):
        if file.endswith('.txt'):
            for line in open(os.path.join(filepath, file), 'r'):
                line = re.sub('[.,!@#$?]', '', line)
                words = line.split()
                words = [word.lower() for word in words]
                [tokens.setdefault(word, file) for word in words]
                if (file in corpus.keys()):
                    corpus[file].append(words)
                else:
                    corpus[file] = words
        elif file.endswith('.json'):
            with open(os.path.join(filepath, file), 'r', encoding='utf-8') as json_file:
                pages = json.load(json_file)
                for page_number, page_content in pages.items():
                    words = [word for word in page_content]
                    
                    # added by sidmishraw
                    from pdf_processing import standardize_words
                    words = standardize_words(words)
                    
                    if (page_number == "Page#1"):
                        [print(word) for word in words]
                    [tokens.setdefault(word, file) for word in words]
                    if (file in corpus.keys()):
                        [corpus[file].append(word) for word in words]
                    else:
                        corpus[file] = words
    return corpus, tokens




def determine_word_positions(words):
    """
    Input is a list of words from a doc.
    Outputs dict of word-[positions] key-value pair dict.
    """
    keyword_positions = []
    cntr = 1
    for word in words:
        keyword_positions.append( (word, cntr) )
        cntr += 1
    term_positions = defaultdict(list)
    for (key, value) in keyword_positions:
        term_positions[key].append(value)
    return sorted(term_positions.items())




def determine_doc_frequency(docs, tokens, corpus):
    """
    Inputs:
        1) Files
        2) Tokens
        3) Corpus
    Flip all 0's to 1's for every word apearing in row's doc
    Outputs a table.
    """
    number_of_rows = len(docs)
    number_of_cols = len(tokens)
    doc_frequency = np.zeros( (number_of_rows, number_of_cols) )
    doc_frequency = pd.DataFrame(
        data=doc_frequency,
        index=np.arange(number_of_rows),
        columns=tokens,
        dtype=int)
    for ind, doc in enumerate(docs):
        # This row should correspond to the doc
        row = doc_frequency.iloc[ind]
        words = corpus[doc]
        for word in words:
            row[word] = 1
    return doc_frequency




def sc_to_word(filepath, filename):
    """
    Reads in csv file output from Simplicial Complex.

    Each row in the csv should contain the following:
        1) # of rules (ie, the simplex order)
        2) frequency of simplex
        3) the simplex members (ie, the tokens making up the simplex)
    """
    with open(os.path.join(os.listdir(filepath), filename)) as csvfile:
        sc_reader = csv.reader(csvfile)
        for line in sc_reader:
            print(line)




