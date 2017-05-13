import gensim
import nltk
import numpy as np
import re
from models.model import Model

class TFIDF_BOG(Model):
    def load_corpus(self, corpus):
        # for this baseline we'll treat the entire corpus as one document
        # then we can compute similarity scores for each of the paras in the new doc
        gen_articles = [[w.lower() for w in nltk.tokenize.word_tokenize(article)] \
            for article in corpus]
        dictionary = gensim.corpora.Dictionary(gen_articles)
        gen_corpus = [dictionary.doc2bow(gen_art) for gen_art in gen_articles]

        tf_idf = gensim.models.TfidfModel(gen_corpus)

        sims = gensim.similarities.Similarity('tmp', tf_idf[gen_corpus],
                                                    num_features=len(dictionary))
        self.dictionary = dictionary
        self.tf_idf = tf_idf
        self.sims = sims
    def highlight(self, article):
        # split article into paragraphs
        # TODO more robust paragraph splitting
        paras = article.split('\n\n')
        paras_split = [[w.lower() for w in nltk.tokenize.word_tokenize(p)] for p in paras]
        # check similarity for each para
        para_tf = [self.tf_idf[self.dictionary.doc2bow(p)] for p in paras_split]
        para_sims = np.sum(self.sims[para_tf], axis=1)

        least_similar = para_sims.argsort()[:4]
        for index in least_similar:
            print(paras[index])

        


        



