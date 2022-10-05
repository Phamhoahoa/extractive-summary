import create_matrix
import pandas as pd 
from nltk import sent_tokenize, word_tokenize, PorterStemmer
import matplotlib.pyplot as plt
import re
import string
from functools import reduce
import math
from math import log
# from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import cluster
from sklearn.cluster import KMeans
from nltk import sent_tokenize, word_tokenize, PorterStemmer
from nltk.corpus import stopwords   
from nltk.cluster import KMeansClusterer
import numpy as np 
from nltk.cluster.util import cosine_distance
import nltk
import numpy as np
from operator import itemgetter
import featureExtraction, preprocessing, settings, readfile
import os
import glob
import errno
import sys

import json

with open('/home/pham.thi.hoa/PycharmProjects/base.vn/textrank/envir.json') as jsonf:
    data = json.load(jsonf)
    
    file_plaintext = data["file_plaintext"]
    
    file_system_textrank = data["file_system_textrank"]
    file_system_KMeans = data["file_system_KMeans"] 


class KmeansCluster(object):
    def Import_KMeans(self,doc):
        # _, doc = readfile.FileReader(path).read_file()
        # doc = readfile.FileReader(path).read_file()
        # print(title)
        sentences = preprocessing.NLP(doc).sentence_segmentation()
        total_documents = len(sentences)
        print(total_documents, end="\n")
        freq_matrix = create_matrix.Create_frequency_matrix(sentences)
        tf_matrix = create_matrix.Create_tf_matrix(freq_matrix)
        count_doc_per_words = create_matrix.Create_documents_per_words(freq_matrix)
        # Calculate IDF and generate a matrix
        idf_matrix = create_matrix.Create_idf_matrix(freq_matrix, count_doc_per_words, total_documents)
        # print(idf_matrix)

        # 6 Calculate TF-IDF and generate a matrix
        tf_idf_matrix = create_matrix.Create_tf_idf_matrix(tf_matrix, idf_matrix)

        
        sentence_scores = create_matrix.Score_sentences(tf_idf_matrix)
        # print(sentence_scores)
        #Creating a dataframe from tfidfmatrix for data processing 
        df = pd.DataFrame(tf_idf_matrix)
        print(np.matrix(df))
        df = df.T

        df.replace(np.nan,0,inplace=True)
        x = df.values
        print(df.values)
       
        print("---------------------------------------------------------------------------")
        x.shape 
    
        # # Apply clustering on the data using sklearn KMeans
      
        kmeans = cluster.KMeans(n_clusters=4, init='k-means++',
                            max_iter=100, n_init=1, verbose=0, random_state=3425)
        kmeans.fit(x)

        labels = kmeans.labels_
        centroids = kmeans.cluster_centers_
        labels
        
        lbl = pd.DataFrame(labels, columns=["label"])
        final_df = df
        final_df['cluster'] = lbl.values
        test = (final_df == 0).astype(int).sum(axis=1)
        test_df = pd.DataFrame(test)
        
        test_df['total'] = 100
        test_df['not_null'] = test_df['total'] - test_df[0]
        
        test_df['cluster'] = final_df['cluster']
        
        test_df.rename(columns={0:"blank_columns"}, inplace=True)
        
        x = pd.DataFrame(test_df.groupby('cluster')['not_null'].sum())
        
        x.rename(columns={"not_null":"Occurrence"}, inplace=True)
        # print(np.matrix(x))
        # print(x)

        y = pd.DataFrame(test_df.groupby('cluster')['not_null'].count())
        y.rename(columns={"not_null":"Not_null_rows"}, inplace=True)
        
        print(y)

        frequency_df_temp = pd.concat([x , y], axis=1)
        # print(np.matrix(frequency_df_temp))
        frequency_df_temp["frequency"] = frequency_df_temp["Occurrence"]/(frequency_df_temp["Not_null_rows"]*100  )

        frequency_df_temp[frequency_df_temp["frequency"] == max(frequency_df_temp["frequency"])].index[0]
        df1 = final_df[final_df.cluster == frequency_df_temp[frequency_df_temp["frequency"] == max(frequency_df_temp["frequency"])].index[0]]
        # print(df1)
        final_dict = df1.set_index(df1.T.columns).T.to_dict('list')
        # print(len(final_dict.keys()))
        l = {}
        
        for i in final_dict.keys():
            for j in sentence_scores.keys():
                if i == j:
                    l[i] = 1
                    
        print(len(l))
        return l 
           

    def summary(self, sentences, sentenceValue):
        sentence_count = 0
        summary = ''
        count_sum = int(len(sentences) / 4)
        for sentence in sentenceValue:
            summary += " " + sentence +"\n"
            sentence_count += 1
            # if sentence_count > count_sum:
            #     break
        print(summary)
        return summary


    def testKmeans(self):
        list_folder = ['khcn', 'CT', 'KT', 'VH' , 'XH','KHGD']
        for folder in list_folder:
            path = file_plaintext + folder+'/*.txt'
            list_of_files = glob.glob(path)

            for file_name in list_of_files:
            
                f = open(file_name, 'r')
                title, doc = readfile.FileReader(file_name).read_file()
                # print(title)
                sentences = preprocessing.NLP(doc).sentence_segmentation()
                l = self.Import_KMeans(file_name)
                summary_text = KmeansCluster().summary(sentences, l)
                # print(summary_text)
                result = title + "\n"
                for _, sent_sum in enumerate(summary_text):
                    result = result + sent_sum 
                f = open(os.path.join(file_system_KMeans + folder +'/',
                os.path.basename(file_name)) , 'w')

                f.write(result)
                f.close()   
                #------------------------------------------------------------------------------------------------------------
    def main(self):
        file_name = "text.txt"
        f = open(file_name, 'r')
        # title, doc = readfile.FileReader(file_name).read_file()
        doc = readfile.FileReader(file_name).read_file()
        sentences = preprocessing.NLP(doc).sentence_segmentation()
        l = self.Import_KMeans(file_name)
        summary_text = KmeansCluster().summary(sentences,l)
        # result = title + "\n"
        result = "\n"
        for _, sent_sum in enumerate(summary_text):
            result = result + sent_sum
        f = open("result.txt", 'w')
        f.write(result)
        f.close()
    def kmeanSummary(self, text):
        sentences = preprocessing.NLP(text).sentence_segmentation()
        l = self.Import_KMeans(text)
        summary_text = KmeansCluster().summary(sentences,l)
        # result = title + "\n"
        result = "\n"
        for _, sent_sum in enumerate(summary_text):
            result = result + sent_sum
        return result 
if __name__ == '__main__':
    # KmeansCluster().testKmeans()
    KmeansCluster().main()
    # file_name = "text.txt"
    # f = open(file_name, 'r')
    # doc = readfile.FileReader(file_name).read_file()      
    # KmeansCluster().kmeanSummary(doc)