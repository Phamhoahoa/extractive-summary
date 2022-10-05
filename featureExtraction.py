from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
import gensim.models as g
import  readfile
model="imdb.d2v"  
import nltk
import preprocessing

class FeatureExtraction(object):
    def __init__(self, doc):
        self.doc = doc

    def tf_idf(self):
        tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0.0)
        tfidf_matrix = tf.fit_transform(self.doc)
        print(tfidf_matrix.shape)
        return tfidf_matrix
    def feature(self):
        m = g.Doc2Vec.load(model)
        sentences = nltk.sent_tokenize(doc)
        sent_vec = np.zeros((1,100))
        vector = []
        numw = 0
        for w in sentences:
            word = preprocessing.NLP().get_words_feature(w)
            print(word)
            sent_vec = m.infer_vector(word)
            
            numw+=1
            vector = np.concatenate((vector, sent_vec), axis=0)
        # vector = m.infer_vector(sentences)
        print(vector.shape)
        return sent_vec / np.sqrt(sent_vec.dot(sent_vec))



