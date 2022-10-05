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
import math
with open('/home/pham.thi.hoa/PycharmProjects/base.vn/textrank/envir.json') as jsonf:
    data = json.load(jsonf)
    
    file_plaintext = data["file_plaintext"]
    
    file_system_textrank = data["file_system_textrank"]
    file_system_KMeans = data["file_system_KMeans"] 

class TextRank(object):
    # def cosine(self, u, v):
    #     if (math.sqrt(np.dot(u, u)) * math.sqrt(np.dot(v, v))) != 0:
    #         return 1 - (np.dot(u, v) / (math.sqrt(np.dot(u, u)) * math.sqrt(np.dot(v, v))))

    def sentence_similarity(self, vector1, vector2):
        return 1 - cosine_distance(vector1, vector2)
        # return 1 - cosine(vector1, vector2)
        
    def build_similarity_matrix(self,sentences_matrix):
        try:
            S = np.zeros((sentences_matrix.shape[0], sentences_matrix.shape[0]))
            for index1 in range(sentences_matrix.shape[0]):
                for index2 in range(sentences_matrix.shape[0]):
                    if index1 == index2:
                        continue
                        # Các phần tử trên đường chéo bằng 0
                    
                    # np.seterr(divide='ignore', invalid='ignore')
                    S[index1][index2] = self.sentence_similarity(sentences_matrix[index1], sentences_matrix[index2])
            # Chuẩn hóa ma trận theo hàng
            for idx in range(len(S)):
                if S[idx].sum() == 0:
                    S[idx] = np.add(S[idx], np.ones(len(S))/(len(S)*10))

                S[idx] /= S[idx].sum()
            return S
        except:
            pass
       
    def pagerank(self, A, eps = 0.001, d = 0.85):
        P = np.ones(len(A)) / len(A)
        while True:
            new_p = np.ones(len(A)) * (1 - d) / len(A) + d *A.T.dot(P)
            delta = abs(new_p - P).sum()
            if delta <= eps:
                return  new_p
            P = new_p
    def textrank(self,sentences, tf_idf_matrix):
        """
        :param sentences: một danh sách các câu [[w11, w12, ...], [w21, w22, ...], ...]
        :param tf_idf_matrix: ma trận mã hóa các câu dạng vector theo tf-idf
        :return: một tuple chứa các câu được xếp hạng giảm dần theo thứ tự
        """
        top_n = (len(sentences) // 2)  #số câu tóm tắt muốn đưa vào văn bản tóm tắt
        S = self.build_similarity_matrix(tf_idf_matrix)
        sentence_ranks = self.pagerank(S)

        # Sắp xếp thứ hạng các câu
        ranked_sentence_indexes = [item[0] for item in sorted(enumerate(sentence_ranks), key=lambda item: -item[1])]
        selected_sentences = sorted(ranked_sentence_indexes[:top_n])
        summary = itemgetter(*selected_sentences)(sentences)
        return summary


    def summary(self, text):
        document = text.split('\n')
        docs = []
        for d in document:
            if d.endswith('.') == False and d != '':
                d = d + '.'
            docs.append(d)
        docs = ' '.join(docs)
        # print(docs)
        sentences = nltk.sent_tokenize(docs)
        # print(sentences)
        doc_parsed = preprocessing.NLP(docs).doc_parsed()
        tf_idf_matrix = featureExtraction.FeatureExtraction(doc_parsed).tf_idf().toarray()
        summary = self.textrank(sentences, tf_idf_matrix)
        # summary = ' '.join(summary)
        return summary

    def main(self,path):
        # title, doc = readfile.FileReader(path).read_file()
        doc = readfile.FileReader(path).read_file()
        sentences = preprocessing.NLP(doc).sentence_segmentation()
        doc_parsed = preprocessing.NLP(doc).doc_parsed()
        tf_idf_matrix = featureExtraction.FeatureExtraction(doc_parsed).tf_idf().toarray()

        summary = self.textrank(sentences, tf_idf_matrix)
        # result = title + "\n"
        result = "\n"
        for _, sent_sum in enumerate(summary):
            result = result + sent_sum + "\n"
        print('use tf-idf model')
        for idx, sentence in enumerate(self.textrank(sentences, tf_idf_matrix)):
            print("%s. %s" % ((idx + 1), sentence))
        return result
    #test data 200 document
    def testsummary(self):
        list_folder = ['khcn', 'CT', 'KT', 'VH' , 'XH','KHGD']
        for folder in list_folder:
            path = file_plaintext + folder+'/*.txt'
            list_of_files = glob.glob(path)

            for file_name in list_of_files:
                print(file_name)
                f = open(file_name, 'r')
                text2 = TextRank().main(file_name)
                f = open(os.path.join(file_system_textrank + folder+'/',
                os.path.basename(file_name)) , 'w')

                f.write(text2)
                f.close()
    # summary contracts -- fail
    def testcontract(self):
        path = 'text-hop-dong'+'/*.txt'
        list_of_files = glob.glob(path)
        for file_name in list_of_files:
            f = open(file_name, 'r')
            text2 = TextRank().main(file_name)
            f = open(os.path.join('summary-hop-dong'+'/',
            os.path.basename(file_name)) , 'w')
            f.write(text2)
            f.close()
        
if __name__ == '__main__':
    # file_name = "text.txt"
    file_name = input("Enter the path of your file: ")
    assert os.path.exists(file_name), "I did not find the file at, "+str(file_name)

    f = open(file_name, 'r')
    text2 = TextRank().main(file_name)
    print(text2)
    f = open("result.txt", 'w')
    f.write(text2)
    f.close()
    #  TextRank().testsummary()
   
    # TextRank().testcontract()
    


