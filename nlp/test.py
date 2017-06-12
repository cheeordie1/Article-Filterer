import argparse
import pickle as pkl
from models.tfidf_bog import TFIDF_BOG
from models.wmd import WMD
from models.sif import SIF
import sys
import csv
from preprocess import preprocess

def print_similarities(paras, sims, scores):
    totalError = 0.0
    n = len(scores)
    for i in range(n):
        print("PARAGRAPH:")
        print(paras[i])
        print("Similarity to known material assigned by algorithm: {}".format(sims[i]))
        print("Similarity to known material assigned by reader's judgement: {}".format(scores[i]))
        error = abs(scores[i]-sims[i])
        print("Error: {}".format(error))
        totalError+=error
    avgError = totalError/n
    print("\nAverage Error for this algorithm and dataset: {}".format(avgError))

    # index = sims.argsort()
    # for ind in index:
    #     print(paras[ind], sims[ind])
    #     print()

def test_corpus(corpus, new_article,scores):
    model = SIF(threshold=0.6, mode= 'section')#TFIDF_BOG()
    model.load_corpus(corpus)
    indices, highlighted = model.highlight(new_article)
    for i in range(len(indices)):
        print(new_article[indices[i][0]:indices[i][1]])
        print(highlighted[i])
#    print_similarities(paras, sims, scores)
    
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

    # load the subjective 'newness' scores from reading the new article
#    with open('data/sample_datasets/%s_paragraph_scores.csv' % name, 'rt') as f:
#        reader = csv.reader(f)
#        paragraph_newness_scores = list(reader)
#        scores = [(5.0-float(s[0]))/5.0 for s in paragraph_newness_scores]
    scores = [0 for i in range(2)]
    #corpus = [
    #        'Jackie Moon\'s mom invented the alley-oop',
    #        'The Golden State Warriors are a basketball team',
    #        'He shot the basketball at the hoop',
    #        ]

    #article = 'My hovercraft is full of eels.  The Golden State Warriors play basketball'

    article = corpus[0]
    corp = corpus[1:]
    print(len(corpus))

#    print(corpus)
#    print(article)
           
    test_corpus(corp, article,scores)

