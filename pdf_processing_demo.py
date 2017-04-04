# pdf_processing_demo.py
# -*- coding: utf-8 -*-
# @Author: Sidharth Mishra
# @Date:   2017-03-06 17:14:07
# @Last Modified by:   Sidharth Mishra
# @Last Modified time: 2017-04-03 19:56:00




__author__ = 'sidmishraw'
__email__ = 'sidharth.mishra@sjsu.edu'




'''
This is a demo for the PDF processing module.
'''



# Python standard library imports
from pprint import pprint
from json import dumps
from json import loads
from pdb import set_trace




# cs_267_project specific imports
from pdf_processing import extract_pages
from pdf_processing import extract_page_contents
from pdf_processing import get_pdf_contents
from pdf_processing import create_json_file
from pdf_processing import extract_words
from pdf_processing import build_pdf_json
from pdf_processing import cleanse_extracted_words
from pdf_processing import cleansed_pdf_json
from pdf_processing.pdf_processor import TEST_PDF
from pdf_processing.pdf_processor import TEST_PDF_2



if __name__ == '__main__':
  '''
  Using the pdf `obscalculi_testing_pdf_conv.pdf` as the sample for the demo.
  '''

  print('Converting pdfs into JSONs and making your life simpler...')

  # creates the JSON file for the PDF document's pages mapped to their contents.
  # create_json_file('phase1.json')

  # Extracts the text from PDF and converts to a JSON preserving the ordering of the words
  # as they were found from the PDF.
  doc_name = TEST_PDF
  get_pdf_contents(TEST_PDF)

  def_dict = extract_words()

  with open('phase3_1.json', 'w') as fp_open:
    fp_open.write(dumps(def_dict))

  def_dict = cleanse_extracted_words(def_dict)

  with open('phase3.json', 'w') as fp_open:
    fp_open.write(dumps(def_dict))

  # Extracts the text from the PDF and groups them together according to their fonts, font-weight,
  # size and behavior in the PDF document. Then cleanses them so the PDF found order is not 
  # maintained but the grouped order is maintained.
  doc_name = TEST_PDF_2
  get_pdf_contents(TEST_PDF_2)

  def_dict = build_pdf_json()

  with open('phase3_2_1.json', 'w') as fp_open:
    fp_open.write(dumps(def_dict))

  def_dict = cleansed_pdf_json(def_dict)

  with open('phase3_2.json', 'w') as fp_open:
    fp_open.write(dumps(def_dict))
