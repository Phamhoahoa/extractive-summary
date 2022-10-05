import os

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DOCUMENT = os.path.join(DIR_PATH, 'document.txt')
PLAINTEXT_PATH = os.path.join(DIR_PATH, 'Plaintext')
SUMMARY_MANUAL_PATH = os.path.join(DIR_PATH, 'Summary_manual')
SUMMARY_SYSTEM_PATH = os.path.join(DIR_PATH, 'Summary_system')
STOP_WORDS = os.path.join(DIR_PATH, 'vietnamese_stopwords.txt')
SPECIAL_CHARACTER = '0123456789%@$.?,=+-!–;/()*"&^:”“#|\n\t\''
DICTIONARY_PATH = 'dictionary.txt'