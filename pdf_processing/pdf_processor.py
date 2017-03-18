# pdf_processor.py
# -*- coding: utf-8 -*-
# @Author: Sidharth Mishra
# @Date:   2017-03-06 16:58:51
# @Last Modified by:   Sidharth Mishra
# @Last Modified time: 2017-03-18 00:25:12




'''
Going back to using `PDFMiner` library by `Yusuke Shinayama`.
However, this time, I'm planning to use only the core PDFDocument and Parser from the module.
Since I'll be customizing the output to fit our requirements, I've decided on this approach.
'''




# python standard library imports
from json import dumps
from json import loads
from pprint import pprint
from re import compile
from re import findall
from re import IGNORECASE
from re import sub
from collections import defaultdict




# PDFMiner library imports
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdftypes import PDFStream




# chardet library imports
from chardet import detect




# Constants that are going to be used through out this script
# These are keys defined in pdfminer module for building the dicts used in the module.
PAGES = 'Pages'
PAGELABELS = 'PageLabels'
METADATA = 'Metadata'
TYPE = 'Type'
CONTENTS = 'Contents'
KIDS = 'Kids'




# Globals
# The global dict that holds the mapping of the page to its corressponding contents.
__pdf_contents_dict__ = {}
TEST_PDF = 'obscalculi_testing_pdf_conv.pdf'
TEST_PDF_2 = '07817034.pdf'




# Toy method
# Fetches the stream objects from the PDFDocument.
def get_stream_objs(doc):
  '''
  Gets the PDFStream objects for the PDFDocument.

  :param: doc `PDFDocument`

  :return: obj_list `list(PDFStream)`
  '''

  obj_list = []

  i = 1
  obj = doc.getobj(i)

  while obj != None:
    if type(obj) == PDFStream:
      print('objid = {}'.format(i))
      obj_list.append(obj)
    i += 1
    try:
      obj = doc.getobj(i)
    except:
      break

  return obj_list




# Toy method
# Decode the stream and get the decoded stream data
def get_stream_data(stream_obj_list):
  '''
  Creates a JSON string after decoding the stream objects.

  :param: stream_obj_list `list(PDFStream)` - The list of PDFStream objects
  that need to be decoded.

  :return: `None`
  '''

  # need to filter the steam objects
  stream_obj_list = list(filter(lambda x: len(x.attrs) == 2, stream_obj_list))

  json_string = {}

  for stream_obj in stream_obj_list:
    # decode the stream obj
    stream_obj.decode()
    json_string[stream_obj.objid] = str(stream_obj.data)

  with open('op_1.json', 'w') as op_f:
    op_f.write(dumps(json_string))

  return




# This function will extract the pages from the PDF document using the PDF's catalog
def extract_pages(pdf_doc):
  '''
  Extract the list of pages from PDF document catalog.
  This will give us all the pages in the PDF document.

  :param pdf_doc: The PDF document from whose catalog we are trying to extract the
  pages from. :class: `pdfminer.pdfdocument.PDFDocument`

  :return pages: The list of pages of the PDF document. :class: `list(dict)`
  '''

  # The catalog is a dict
  # we are only interested in the `Pages` key and its value.
  # `Pages` has a list of `pdfminer.pdftypes.PDFObjRef` as its value.
  catalog = pdf_doc.catalog

  # The list of pages that needs to be returned
  pages = []

  # looping through the page references in the catalog and resolving them before
  # adding to the list to be returned from this function.
  # catalog[PAGES] gives the object references to the Pages listing
  for objref in catalog[PAGES].resolve()[KIDS]:
    pages.append(objref.resolve())

  return pages




# Extract contents of the pages
def extract_page_contents(page_nbr, page):
  '''
  Extract the contents of a page. By iterating over the Contents list of a page of the PDF document,
  we will build a dict for the PDF contents.

  :param page_nbr: The page number as per the PDF catalog. :class: `int`
  :param page: The PDF page dict obtained from the catalog of the PDF document. :class: `dict`

  :return: `None`
  '''

  global __pdf_contents_dict__

  # contents is the list of `pdfminer.pdftypes.PDFStream` objects.
  contents = []

  # page dict is the dict constructed per page to hold the mapping from
  # page number to the decoded contents of that page.
  page_dict = {}

  # looping through the `pdfminer.pdftypes.PDFObjRef`s in the Contents list of the page
  # and adding the resolved PDFStream objects to the contents list
  if type(page[CONTENTS]) != list:
    contents.append(page[CONTENTS].resolve())
  else:
    for objref in page[CONTENTS]:
      contents.append(objref.resolve())

  # contruct the page_dict
  # The value is converted to string since the JSON conversion of bytes is hard.
  # using chardet's detection of encoding, encode the bytes into the str format
  # using the detected encoding.
  for index, stream_obj in enumerate(contents):
    stream_obj.decode()
    chardet_detected_encoding = detect(stream_obj.data)['encoding']
    page_dict['Content#{}'.format(index)] = str(stream_obj.data, \
      encoding = chardet_detected_encoding)

  # contruct the __pdf_contents_dict__
  __pdf_contents_dict__['Page#{}'.format(page_nbr)] = page_dict

  return




# The accessor for the __pdf_contents_dict__
def get_pdf_contents(pdf_file_name):
  '''
  Takes the PDF file name(qualified name) and returns the mapping of the contents of the pages of
  the PDF document. The contents of the PDF document is extracted from the Catalog of the 
  PDF document.

  The accessor function for the __pdf_contents_dict__. This is done deliberately to prevent
  modification of the dict by any other means.

  :param pdf_file_name: The Qualified File Path (file name with .pdf extension) of the PDF document
  whose contents are needed. :class: `str`

  :return: The copy of the __pdf_contents_dict__ so that it isn't modified by 
  other operations. :class: `dict`
  '''

  global __pdf_contents_dict__

  # The PDF parser - `pdfminer.pdfparser.PDFParser`
  parser = None

  with open(pdf_file_name, 'rb') as ip_file:
    # get the parser instance from the open file
    parser = PDFParser(ip_file)

    # get the parsed PDFDocument instance
    doc = PDFDocument(parser)

    # extracting pages from the PDF document
    pages = extract_pages(doc)

    # building the pdf_contents_dict by parsing all the pages of the PDF
    for page_nbr, page in enumerate(pages):
      extract_page_contents(page_nbr + 1, page)

  return dict(__pdf_contents_dict__)




# Writes the Page:Contents mapping to the JSON file
# Writing to a JSON file can help if we need to use someother platform/stack for this program.
def create_json_file(json_file_name):
  '''
  Creates the JSON file from the global dict (pdf_contents_dict) that contains the mapping from the
  page to its corressponding contents. It takes the file name for the JSON file as argument.

  :param json_file_name: The file name of the JSON file created. :class: `str`

  :return: None
  '''

  global __pdf_contents_dict__

  json_string = dumps(__pdf_contents_dict__)

  with open(json_file_name, 'w') as op_file:
    op_file.write(json_string)

  return




# finds all the matching patterns to the provided regex pattern
def __find_all_matching__(regex_pattern, search_text):
  '''
  Finds and returns all the matching regex patterns.

  :param regex_pattern: The regex pattern :class: `_sre.SRE_Pattern`
  :param search_text: The string to search on. :class: `str`

  :return: matches `list(str)`
  '''

  matches = findall(regex_pattern, search_text)
  
  return matches




# Trying to parse the PDF and make the metadata for the entire PDF
# {
#   "Page#1": {
#     "Content#0": {},
#     "Content#1": {},
#     "Content#2": {
#       "/T1_0#1#13.948": [
#         [
#           "Learning",
#           "Embedding",
#           "Representations",
#           "for",
#           "Knowledge",
#           "Inference",
#           ...]
#           ...]
#           ...
#     },
#     ...
# }
# and
# {
#   "Page#1": [
#     "Observational",
#     "Calculi,",
#     "Classes",
#     "of",
#     ...]
#     ...
# }
# formats.
def __build_pdf_json_pattern__():
  '''
  Builds and returns the regex pattern to extract the information from the contents of the PDF
  pages.

  :return: pattern `_sre.SRE_Pattern`
  '''

  # compile this long regex for extracting information from the page contents
  regex_font_name = r'(?P<font_name>/T\d_\d)'
  regex_font_size = r'(?P<size>\d)'
  regex_font_weight = r'(?P<weight>[\-|\+]{0,1}\d*\.{0,1}\d*)'
  regex_text_group = r'(\[.*?\]|\(.*?\))'

  # compound regex pattern since it is too long
  regex_pattern_string = r'(%s\s%s\sTf\s%s\s*?.*?\s*?.*?%s)|%s' % (regex_font_name, \
    regex_font_size, regex_font_weight, regex_text_group, regex_text_group)

  pattern = compile(regex_pattern_string, IGNORECASE)

  return pattern




# def __extract_content__(matching_pattern):
#   '''
#   Extracts the text from the PostScript code.

#   :return: extracted_text `str`
#   '''

#   text_pattern = r'\((.*?)\)'
#   text_pieces = findall(compile(text_pattern), matching_pattern)

#   return ''.join(text_pieces)




def __extract_content__(matching_pattern):
  '''
  New and improved. Text extraction mechanism.

  :return: extracted_text `list(str)`
  '''

  text_digit_regex_pattern = r'(-{0,1}\d*)\((.*?)\)'
  matching_patterns = findall(compile(text_digit_regex_pattern), matching_pattern)

  extracted_texts = []
  extracted_string = ''

  for pattern in matching_patterns:
    if pattern[0] == '':
      extracted_string = pattern[1]
    elif float(pattern[0]) >= 0:
      extracted_string = '{}{}'.format(extracted_string, pattern[1])
    elif float(pattern[0]) < 0:
      extracted_texts.append(extracted_string)
      extracted_string = pattern[1]

  extracted_texts.append(extracted_string)

  return extracted_texts




# Text extractor
def __get_content__(content):
  '''
  Extracts the textual contents from the PostScript code decompressed from PDF page.

  :param content: The decompressed PostScript code from the PDF page. :class: `str`

  :return: contents `dict`
  '''

  # get the pattern that will parse the contents of the PDF page
  regex_pattern = __build_pdf_json_pattern__()

  contents = defaultdict(list)

  matching_patterns = findall(regex_pattern, content)

  index = -1
  seeker = 0

  while index < len(matching_patterns) and seeker < len(matching_patterns):

    if matching_patterns[seeker][5] == '':
      index = seeker

    contents_key = '{}#{}#{}'.format(matching_patterns[index][1], \
        matching_patterns[index][2], matching_patterns[index][3])

    if matching_patterns[seeker][5] == '':
      contents[contents_key].append(__extract_content__(matching_patterns[seeker][4]))
    else:
      contents[contents_key].append(__extract_content__(matching_patterns[seeker][5]))

    seeker += 1

  return contents




# EXPERIMENTAL - Testing1 complete - can use now
# Builds the JSON structure for the PDF
def build_pdf_json():
  '''
  `The reading order of the words is not preserved but the grouping order is preserved.`
  Extracts the text and groups similar text together depending on their font, size, weight behavior
  in the pdf document. For this reason their reading order is not preserved but they get logically
  grouped based on their roles in the document.

  :return: pdf_dict `dict`
  '''

  global __pdf_contents_dict__

  pdf_dict = {}

  # {'Page#x':{'Content#y':""}}
  for page, contents in __pdf_contents_dict__.items():
    pdf_dict[page] = {}
    for content_key, content in contents.items():
      pdf_dict[page][content_key] = __get_content__(content)

  return pdf_dict




# findall(compile(r'\b[\W]*([\w\W]+)[\W]*\b'), '--F-Property;;')
# ['default', 'mmmm', '']
def __leading_trailing_nonword_remover__(word_string):
  '''
  Removes the leading and trailing non-word i.e `\W` from the strings cleansing them.

  :param word_string: The word to be cleansed. :class: `str`

  :return: word `str`
  '''

  word = findall(compile(r'\b[\W]*([\w\W]+)[\W]*\b'), word_string)

  if len(word) == 0:
    return ''
  else:
    return word[0]




def __cleanse_words__(word_group, cleansed_word_container):
  '''
  Cleanse the words by removing hypenations, commas, periods etc from the end of the words and
  clean them all.

  :param word_group: The words in the word_group :class: `list(str)`
  :param cleansed_word_container: The container to hold the cleansed words :class: `list(str)`

  :return: None
  '''

  for word in word_group:
    if len(cleansed_word_container) != 0 and cleansed_word_container[-1].endswith('-'):
      cleansed_word_container[-1] = '{}{}'.format(cleansed_word_container[-1][:-1], word)
    else:
      cleansed_word_container.append(word)

  return




# cleansed pdf json aka a python dict
def __dump_words__(content_group, cleansed_page_contents):
  '''
  Extracts and dumps the words inside the content groups of the PDF-JSON's pages into the
  `cleansed_page_contents`

  :param content_group: The content group, i.e, the value portion of the "Content#1": {...} 
  :class: `dict`
  :param cleansed_page_contents: The cleansed page contents (transformed words 
  are written into this list) :class: `list(str)`

  :return: None
  '''

  for word_group in content_group:
    __cleanse_words__(word_group, cleansed_page_contents)

  return




def __cleanse_page_contents__(page_contents):
  '''
  Cleanses the contents of the page and returns a list of stemmed words from the contents of the page.

  :param page_contents: The contents of the page :class: `dict`

  :return: cleansed_page_contents `list(str)`
  '''

  cleansed_page_contents = []

  for content_groups in page_contents.values():
    for content_group in content_groups.values():
      __dump_words__(content_group, cleansed_page_contents)

  cleansed_page_contents = list(map(__leading_trailing_nonword_remover__, cleansed_page_contents))

  return cleansed_page_contents




def cleansed_pdf_json(pdf_dict):
  '''
  `The reading order of the words is not preserved but the grouping order is preserved.`
  The second pass that cleans the PDF JSON structure to make a listing of the words in just pages.
  This phase stems the words using the Porter stemmer algorithm, it also removes the words that are
  not in proper encoding (like \\\028 etc.).

  :param pdf_dict: The pdf_json (python) `dict` object obtained from the build_pdf_json(). 
  :class: `dict`

  :return: cleansed_pdf_dict `dict`
  '''

  cleansed_pdf_dict = {}

  for page_key, page_contents in pdf_dict.items():
    cleansed_pdf_dict[page_key] = __cleanse_page_contents__(page_contents)

  return cleansed_pdf_dict




# Extract the words/phrases from the contents of the __pdf_contents_dict__ and
# make a new pdf_json without grouping the words together and preserving their position in the
# pdf.
def extract_words():
  '''
  Extracts the words(textual)/phrases from the decoded(decomoressed) contents of the PDF pages
  and returns a python dict holding the mapping from page#number to the words in the page.

  :return: pdf_page_words_dict `defaultdict`
  '''

  global __pdf_contents_dict__

  pdf_page_words_dict = defaultdict(list)

  regex_pattern = __build_pdf_json_pattern__()

  for page, page_contents in __pdf_contents_dict__.items():
    for content in page_contents.values():
      matching_patterns = findall(regex_pattern, content)
      for matching_pattern in matching_patterns:
        if matching_pattern[5] == '':
          pdf_page_words_dict[page].extend(__extract_content__(matching_pattern[4]))
        else:
          pdf_page_words_dict[page].extend(__extract_content__(matching_pattern[5]))

  return pdf_page_words_dict




# to be called after extracting words
def cleanse_extracted_words(pdf_page_words_dict):
  '''
  The next phase after obtaining pdf_page_words_dict from `extract_words()`. This will cleanse the
  words removing hypenation and other symbols at the start or end of the words.

  :param pdf_page_words_dict: The dict holding the mapping between page# and it's words.
  :class: `defaultdict`

  :return: cleansed_pdf_page_words_dict `dict`
  '''

  cleansed_pdf_page_words_dict = defaultdict(list)

  for page, page_contents in pdf_page_words_dict.items():
    cleansed_pdf_page_words_dict[page].extend(\
      list(map(__leading_trailing_nonword_remover__, page_contents)))

  return cleansed_pdf_page_words_dict




## IDEA - 03-16, upon further observation of the PDF contents, the numbers < 0 after `()` in the
# postscript code happen to correspond to whitespaces and numbers > 0 are just minor spacing which
# are not word boundaries.
# I'm going to try and leverage this to get meaningful words.




if __name__ == '__main__':
  '''
  Using PDFMiner lib's PDFParser get all the stream objects.
  The stream objects that have only 2 attributes are of interest since they contain
  the text needed by us.

  Hence, the procedure should include a way of filtering them out from the list of
  stream objects. Also we need to decode the rawdata(zlib format compressed data) and then fetch the
  decoded data.

  '''

  # do nothing when this module is run directly.
  pass

  