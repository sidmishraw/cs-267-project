# pdf_downloader_script.py
# -*- coding: utf-8 -*-
# @Author: Sidharth Mishra
# @Date:   2017-03-21 09:55:58
# @Last Modified by:   Sidharth Mishra
# @Last Modified time: 2017-04-03 19:54:17




__author__ = 'sidmishraw'
__email__ = 'sidharth.mishra@sjsu.edu'




'''
This script converts the 20 pdfs from the IEEE Xplore website to JSON. These PDFs will be used as data for the
project. 
'''




# Python Standard library imports
from json import loads
from json import dumps
from os.path import dirname
from os import getcwd
from os import listdir
from os.path import sep




# Project specific imports
from pdf_processing import get_pdf_contents
from pdf_processing import extract_words
from pdf_processing import cleanse_extracted_words
from pdf_processing import build_pdf_json
from pdf_processing import cleansed_pdf_json




def generate_jsons():
  '''
  Generates the JSONs for the pdfs in `input_pdfs` folder into `pdf_jsons` and `pdf_grouped_jsons`
  folders.

  :return: `None`
  '''

  dir_path = '{base_path}{separator}{folder_name}'.format(base_path = getcwd(), separator = sep, \
    folder_name = 'input_pdfs')

  for file_name in listdir(dir_path):
    
    ip_file_path = '{dir_path}{separator}{file_name}'.format(dir_path = dir_path, separator = sep, \
      file_name = file_name)
    
    # decompress the PDF and get the decoded data from the PDF
    def_dict = get_pdf_contents(ip_file_path)

    # PDF reading order of words maintained
    def_dict = cleanse_extracted_words(extract_words())
    
    op_file_path = '{base_path}{separator}{folder_name}{separator}{file_name}'.format(\
      base_path = getcwd(), separator = sep, folder_name = 'pdf_jsons', \
      file_name = '{}.json'.format(file_name.split('.')[0]))
    
    with open(op_file_path, 'w') as fp_open:
      fp_open.write(dumps(def_dict))

    # # PDF grouping of words maintained
    # def_dict = get_pdf_contents(ip_file_path)
    def_dict = cleansed_pdf_json(build_pdf_json())

    op_file_path = '{base_path}{separator}{folder_name}{separator}{file_name}'.format(\
      base_path = getcwd(), separator = sep, folder_name = 'pdf_grouped_jsons', \
      file_name = '{}.json'.format(file_name.split('.')[0]))
    
    with open(op_file_path, 'w') as fp_open:
      fp_open.write(dumps(def_dict))




if __name__ == '__main__':
  print('Using the pdfs in `input_pdfs` folder and building the JSONs in `pdf_jsons` \
    and `pdf_grouped_jsons` folders.')
