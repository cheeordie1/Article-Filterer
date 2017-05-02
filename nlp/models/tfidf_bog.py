import gensim
import nltk
from model import Model

class TFIDF_BOG(Model):
    def load_corpus(corpus):
        gen_articles = [[w.lower() for w in nltk.tokenize.word_tokenize(article['text'])
            for article in corpus]]
        print(gen_articles)
    def highlight(article):
        pass

# basic tests
if __name__ == '__main__':

    model = TFIDF_BOG()
    model.load_corpus()


