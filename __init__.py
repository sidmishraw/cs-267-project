from apriori.build_tables import *
from simplicial_complex.sc_wrapper import SimplicialComplex

"""
Building tables
"""

# Input filepaths
filepath = './inputs/first_test'
# filepath = './inputs/second_test'

if __name__ == '__main__':
    # --------------------------------------------------------------------------------------------------
    # Read in data & init
    (corpus, tokens) = read_input_files(filepath)
    token_list = list(tokens.keys())
    docs = sorted(corpus.keys())

    # --------------------------------------------------------------------------------------------------
    # Part 1 section:  tf
    term_frequency_with_positions = dict()
    for doc in docs:
        term_frequency_with_positions[doc] = determine_word_positions(corpus[doc])
    tf_output = term_frequency_with_positions

    # Print to json file & prettify
    tf_file_output = open('./outputs/output_term_freq.json', 'w')
    tf_file_output.write(json.dumps(tf_output, sort_keys=True, indent=2))

    # --------------------------------------------------------------------------------------------------
    # Part 2 section:  df
    df_output = determine_doc_frequency(docs, token_list, corpus)

    # Print to csv file
    df_output.to_csv('./outputs/output_doc_freq.csv', header=token_list, sep=',')

    # Print to txt file
    np.savetxt('./outputs/output_doc_freq.txt', df_output.values, fmt='%d')

    # --------------------------------------------------------------------------------------------------
    # Part 3 section:  to sc
    sc = SimplicialComplex(4, 0.05, len(tf_output), len(docs))























