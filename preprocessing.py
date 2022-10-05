from pyvi import ViTokenizer
from readfile import FileReader
import settings
import nltk

from sklearn.decomposition import PCA
import numpy as np
import readfile



class NLP(object):
    def __init__(self, doc = None):
        self.doc = doc
        self.__set_stopwords()

    def __set_stopwords(self):
        self.stopwords = FileReader(settings.STOP_WORDS).read_stopwords()

    def sentence_segmentation(self):
        sents_tokened = nltk.sent_tokenize(self.doc)
        return [sent_tokened for sent_tokened in sents_tokened if (sent_tokened not in settings.SPECIAL_CHARACTER and sent_tokened !='.')]

    def word_segmentation(self, sent):
        return ViTokenizer.tokenize(sent)

    def split_words(self, sent):
        sent = self.word_segmentation(sent)
        try:
            step_1 = [x.strip(settings.SPECIAL_CHARACTER).lower() for x in sent.split()]
            return [x for x in step_1 if x != '']
        except TypeError:
            return []

    def get_words_feature(self,sent):
        split_words = self.split_words(sent)
        words = []
        for word in split_words:
            if word not in self.stopwords:
                words.append(word)
        return words

    def doc_parsed(self):
        doc_parsed = []
        sentences = self.sentence_segmentation()
        for sent in sentences:
            sent_parsed = ' '.join(self.get_words_feature(sent))+"."
            if sent_parsed != '.':
                doc_parsed.append(sent_parsed)
        return doc_parsed
#     def embedding_word(self):
#         model = KeyedVectors.load('./pretrain_model/word2vec_skipgram.model')
#         X = np.zeros((25000,))
#         a = NLP().split_words("học bơi đi bạn không thất vọng đâu")
#         print(a)
#         for i in a:
#             X = model[i]
#             print(X)
#             print(X.shape)
#         return []
    
#     def main(self):
#          NLP().embedding_word()
# if __name__ == '__main__':
#     NLP().main()