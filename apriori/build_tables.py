"""
Builds the following tables:
    1) (Dict) Alphabetically ordered words for each document and their positions.
    2) (Bit-Matrix) Alphabetically ordered words across all documents and which
    documents each occurs in.

Created on 2/25/2017

@author: sordonia
"""

import os, re, json
from collections import defaultdict, OrderedDict
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

"""
Run tests here.
"""
# filepath = '../inputs/first_test'
filepath = '../inputs/second_test'
(corpus, tokens) = read_input_files(filepath)
token_list = list(tokens.keys())
docs = sorted(corpus.keys())

# --------------------------------------------------------------------------------------------------
# Part 1 section:  tf

term_frequency_with_positions = dict()
for doc in docs:
    term_frequency_with_positions[doc] = determine_word_positions(corpus[doc])

print("\nThese are the terms with their positions in each doc:\n")
tf_output = term_frequency_with_positions
print(tf_output)
tf_file_output = open('output_term_freq.json', 'w')
tf_file_output.write(json.dumps(tf_output, sort_keys=True, indent=2))

# --------------------------------------------------------------------------------------------------
# Part 2 section:  df

# print("\nThese are the doc frequencies for all terms:\n")
df_output = determine_doc_frequency(docs, token_list, corpus)

# Print to csv file
df_output.to_csv('./output_doc_freq.csv', header=token_list, sep=',')

# Print to txt file
np.savetxt('./output_doc_freq.txt', df_output.values, fmt='%d')


# --------------------------------------------------------------------------------------------------
# Part 3 section:  to sc

# for ind, doc in enumerate(df_output):
#     print(doc)






















