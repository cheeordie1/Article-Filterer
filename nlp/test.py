import argparse
import pickle as pkl
from models.tfidf_bog import TFIDF_BOG
from models.wmd import WMD
import sys

def print_similarities(paras, sims):
    index = sims.argsort()
    for ind in index:
        print(paras[ind], sims[ind])
        print()

def test_corpus(corpus, new_article):
    model = TFIDF_BOG()
    model.load_corpus(corpus)
    paras, sims = model.highlight(new_article)
    print_similarities(paras, sims)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--corpus-name', default='tuval')
    args = parser.parse_args()

    name = args.corpus_name

    print('Testing on %s corpus' % name)
    # load corpus
    with open('data/sample_datasets/%s.pkl' % name, 'rb') as f:
        corpus = pkl.load(f)
        corpus = [art['text'] for art in corpus]

    #corpus = [
            #'Jackie Moon\'s mom invented the alley-oop',
            #'The Golden State Warriors are a basketball team',
            #'He shot the basketball at the hoop',
            #]

    #article = 'My hovercraft is full of eels\n\n The Golden State Warriors play basketball'

    article = corpus[-1]
    corp = corpus[:-1]

    #print(corpus)
    #print(article)
           
    test_corpus(corp, article)

