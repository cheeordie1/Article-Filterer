import gensim
import nltk
import numpy as np
import re
from models.model import Model
from gensim.models.keyedvectors import KeyedVectors
from gensim.similarities import WmdSimilarity

def preprocess(corpus):
    return [[w.lower() for w in nltk.tokenize.word_tokenize(article)  \
            if w not in nltk.corpus.stopwords.words('english')] \
            for article in corpus]

class WMD(Model):
    def load_corpus(self, corpus):
        # TODO cut down on the size of this to speed everything up

        gen_articles = preprocess(corpus)

        model = KeyedVectors.load('data/word2vec/word_vectors.out')
        # normalize word vectors
        model.init_sims(replace=True)
        self.instance = WmdSimilarity(gen_articles, model)

    def highlight(self, article):
        # split article into paragraphs
        # TODO more robust paragraph splitting
        paras = article.split('\n\n')
        # check similarity for each para
        paras_pre = preprocess(paras)
        print('Checking similarity')
        sims = self.instance[paras_pre]

        sims = np.sum(sims, axis=1)

        least_similar = sims.argsort()[:4]
        for index in least_similar:
            print(paras[index])

        


        



