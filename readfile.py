import nltk
import settings
import os
import glob
import errno
import sys

class FileReader(object):
    def __init__(self, file_path):
        self.file_path = file_path

    def read_file(self):
        rows = []
        with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
            file = f.readlines()
        for i, row in enumerate(file):
            if row != '\n':
                row = row.replace('\n', '')
                if row.endswith('.') == False:
                    row = row + '.'
                if i == 0:
                    title = row
                rows.append(row)
        doc_content = ' '.join(rows)
        # return title, doc_content
        return doc_content

    def read_stopwords(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            stopwords = list(set([w.strip().replace(' ', '_') for w in f.readlines()]))
        return stopwords
    
    def read_folder(self, path):
        # path = '/home/pham.thi.hoa/PycharmProjects/base.vn/textrank/Plaintext/boKHCN/*.txt'
        files = glob.glob(path)
        for name in files:
            try:
                with open(name) as f:
                    sys.stdout.write(f.read())
            except IOError as exc:
                if exc.errno != errno.EISDIR:
                    raise



