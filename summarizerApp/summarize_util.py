"""
    Custom utility class to hold custom functions, by degee
"""
import calendar
import datetime
# from Crypto.Cipher import AES
import base64
from os import path
import os
import io
from django.core import serializers
from collections.abc import Iterable
from django.db.models.query import QuerySet
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import re

# import docx
import PyPDF2
import docx2txt

from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

import nltk
import heapq
import textract


class SummarizeUtil:

    def summarize(document, max_sentences=10):
        if document.file.url.endswith('pdf'):
            fileInfo = SummarizeUtil.pdf_to_text(document)
        else:
            fileInfo = SummarizeUtil.docx_to_text(document)
        pages = fileInfo['pages']
        # print("text", fileInfo['text'])
        text = SummarizeUtil.clean_text(fileInfo['text'])
        sentence_list = nltk.sent_tokenize(text)
        token_list = nltk.word_tokenize(text)

        if len(token_list) < 1:
            return {'pages': 0, 'summary': "Invalid document"}

        # print("token_list", len(token_list))
        # print("sentence_list", len(sentence_list))

        stopwords = nltk.corpus.stopwords.words('english')
        word_frequencies = {}
        for word in token_list:
            if word not in stopwords:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1

        maximum_frequncy = max(word_frequencies.values())
        for word in word_frequencies.keys():
            word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

        sentence_scores = {}
        for sent in sentence_list:
            for word in nltk.word_tokenize(sent.lower()):
                if word in word_frequencies.keys():
                    if len(sent.split(' ')) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word]
                        else:
                            sentence_scores[sent] += word_frequencies[word]

        # top 10 sentences with the highest scores
        summary_sentences = heapq.nlargest(
            max_sentences, sentence_scores, key=sentence_scores.get)
        summary = ' '.join(summary_sentences)
        # print(summary)
        return {'pages': pages, 'summary': summary}

    @staticmethod
    def clean_text(text):
        # text = re.sub(r'[[0-9]*]', ' ', text)
        # text = re.sub(r's+', ' ', text)
        # text = re.sub('[^a-zA-Z]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text

    @staticmethod
    def docx_to_text(document):
        path = str(settings.BASE_DIR) + document.file.url
        text = docx2txt.process(path)
        # text = textract.process(path)
        return {'pages': 0, 'text': text}

    @staticmethod
    def pdf_to_text(document):
        path = str(settings.BASE_DIR) + document.file.url
        # print("path", path)
        pages = 0
        scanned_pages = 0
        start_page =  1
        end_scan_page = 200
        if document.start_scan_page:
            start_page =  document.start_scan_page
        if document.end_scan_page:
            end_scan_page = document.end_scan_page
        with open(path, 'rb') as fp:
            rsrcmgr = PDFResourceManager()
            outfp = io.StringIO()
            laparams = LAParams()
            device = TextConverter(rsrcmgr, outfp, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.get_pages(fp):
                pages += 1
                if pages >= start_page and pages < end_scan_page:
                    scanned_pages += 1
                    interpreter.process_page(page)
        text = outfp.getvalue()
        # return text.replace('\t', ' ')
        return {'pages': scanned_pages, 'text': text}

    @staticmethod
    def pdf(file):  # 'example.pdf'
        # creating a pdf File object
        pdfFileObj = open(settings.BASE_DIR + file, 'rb')

        # creating a pdf Reader object
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

        # printing number of pages in pdf file
        # print('number of pages ', pdfReader.numPages)

        # creating a page object
        pageObj = pdfReader.getPage(1)

        # extracting text from page
        # print(pageObj.extractText())

        # closing the pdf file object
        pdfFileObj.close()
