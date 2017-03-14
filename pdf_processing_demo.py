# pdf_processing_demo.py
# -*- coding: utf-8 -*-
# @Author: Sidharth Mishra
# @Date:   2017-03-06 17:14:07
# @Last Modified by:   Sidharth Mishra
# @Last Modified time: 2017-03-14 09:53:44




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
from pdf_processing.pdf_processor import extract_pages
from pdf_processing.pdf_processor import extract_page_contents
from pdf_processing.pdf_processor import get_pdf_contents
from pdf_processing.pdf_processor import create_json_file
from pdf_processing.pdf_processor import extract_words
from pdf_processing.pdf_processor import build_pdf_json
from pdf_processing.pdf_processor import TEST_PDF_2



if __name__ == '__main__':
  '''
  Using the pdf `obscalculi_testing_pdf_conv.pdf` as the sample for the demo.
  '''

  doc_name = 'obscalculi_testing_pdf_conv.pdf'
  pprint(get_pdf_contents(doc_name))
  
  # creates the JSON file for the PDF document's pages mapped to their contents.
  create_json_file('phase1.json')

  # creates the next phase of JSON file that has the text only from the decoded streams
  json_string = extract_words('phase2.json')
  pprint(json_string)

  def_dict = build_pdf_json()

  with open('phase3.json', 'w') as fp_open:
    fp_open.write(dumps(def_dict))

  doc_name = TEST_PDF_2
  get_pdf_contents(TEST_PDF_2)

  def_dict = build_pdf_json()

  with open('phase3_2.json', 'w') as fp_open:
    fp_open.write(dumps(def_dict))





