import re
import string
# import pandas as pd
from functools import reduce
from math import log


import math

from nltk import sent_tokenize, word_tokenize, PorterStemmer
from nltk.corpus import stopwords   

from nltk.cluster import KMeansClusterer

def Create_frequency_matrix(sentences):
    frequency_matrix = {}
    stopWords = set(stopwords.words("english"))
    ps = PorterStemmer()

    for sent in sentences:
        freq_table = {}
        words = word_tokenize(sent)
        for word in words:
            word = word.lower()
            word = ps.stem(word)
            
            word=re.sub("(\\t)", ' ', str(word)).lower() #remove escape charecters
            word=re.sub("(\\r)", ' ', str(word)).lower() 
            word=re.sub("(\\n)", ' ', str(word)).lower()

            word=re.sub("(__+)", '', str(word)).lower()   #remove _ if it occors more than one time consecutively
            word=re.sub("(--+)", '', str(word)).lower()   #remove - if it occors more than one time consecutively
            word=re.sub("(~~+)", '', str(word)).lower()   #remove ~ if it occors more than one time consecutively
            word=re.sub("(\+\++)", '', str(word)).lower()   #remove + if it occors more than one time consecutively
            word=re.sub("(\.\.+)", '', str(word)).lower()   #remove . if it occors more than one time consecutively

            word=re.sub(r"[<>()|&©ø\[\]\'\",;?~*!’. ]", '', str(word)).lower() #remove <>()|&©ø"',;?~*!

            word=re.sub("(mailto:)", '', str(word)).lower() #remove mailto:
            word=re.sub(r"(\\x9\d)", '', str(word)).lower() #remove \x9* in text
            word=re.sub("([iI][nN][cC]\d+)", 'INC_NUM', str(word)).lower() #replace INC nums to INC_NUM
            word=re.sub("([cC][mM]\d+)|([cC][hH][gG]\d+)", 'CM_NUM', str(word)).lower() #replace CM# and CHG# to CM_NUM


            word=re.sub("(\.\s+)", '', str(word)).lower() #remove full stop at end of words(not between)
            word=re.sub("(\-\s+)", '', str(word)).lower() #remove - at end of words(not between)
            word=re.sub("(\:\s+)", '', str(word)).lower() #remove : at end of words(not between)
            
            word = re.sub(r"\d+'", '', str(word)).lower() #Remove numbers
            word = word.strip()
            

            word = re.sub("(\s+)",'',str(word)).lower() #remove multiple spaces

            #Should always be last
            word=re.sub("(\s+.\s+)", '', str(word)).lower() #remove any single charecters hanging between 2 spaces
            
            
            if word in stopWords:
                continue

            if word in freq_table:
                freq_table[word] += 1
            else:
                freq_table[word] = 1

        frequency_matrix[sent[:]] = freq_table

    return frequency_matrix
# tạo ma trận tf
def Create_tf_matrix(freq_matrix):
    tf_matrix = {}

    for sent, f_table in freq_matrix.items():
        tf_table = {}

        count_words_in_sentence = len(f_table)
        for word, count in f_table.items():
            tf_table[word] = count / count_words_in_sentence

        tf_matrix[sent] = tf_table

    return tf_matrix

def Create_documents_per_words(freq_matrix):
    word_per_doc_table = {}

    for _, f_table in freq_matrix.items():
        for word, _ in f_table.items():
            if word in word_per_doc_table:
                word_per_doc_table[word] += 1
            else:
                word_per_doc_table[word] = 1

    return word_per_doc_table


def Create_idf_matrix(freq_matrix, count_doc_per_words, total_documents):
    idf_matrix = {}

    for sent, f_table in freq_matrix.items():
        idf_table = {}

        for word in f_table.keys():
            idf_table[word] = math.log10(total_documents / float(count_doc_per_words[word]))

        idf_matrix[sent] = idf_table

    return idf_matrix

def Create_tf_idf_matrix(tf_matrix, idf_matrix):
    tf_idf_matrix = {}

    for (sent1, f_table1), (sent2, f_table2) in zip(tf_matrix.items(), idf_matrix.items()):

        tf_idf_table = {}

        for (word1, value1), (word2, value2) in zip(f_table1.items(),
                                                    f_table2.items()):  # here, keys are the same in both the table
            tf_idf_table[word1] = float(value1 * value2)

        tf_idf_matrix[sent1] = tf_idf_table

    return tf_idf_matrix

def Score_sentences(tf_idf_matrix) -> dict:
    """
    score a sentence by its word's TF
    Basic algorithm: adding the TF frequency of every non-stop word in a sentence divided by total no of words in a sentence.
    :rtype: dict
    """

    sentenceValue = {}

    for sent, f_table in tf_idf_matrix.items():
        total_score_per_sentence = 0

        count_words_in_sentence = len(f_table)
        for word, score in f_table.items():
            total_score_per_sentence += score

        sentenceValue[sent] = total_score_per_sentence / count_words_in_sentence

    return sentenceValue