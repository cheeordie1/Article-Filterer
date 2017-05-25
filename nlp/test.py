import argparse
import pickle as pkl
#from models.tfidf_bog import TFIDF_BOG
#from models.wmd import WMD
from models.sif import SIF

def test_corpus(name):
    print('Testing on %s corpus' % name)
    # load corpus
    with open('data/sample_datasets/%s.pkl' % name, 'rb') as f:
        corpus = pkl.load(f)
        corpus = [d['text'] for d in corpus]

    model = SIF(1, 1, 1, 1000)#TFIDF_BOG()
    model.load_corpus(corpus)
    model.highlight(corpus[0])
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--corpus-name', default='gsw')
    args = parser.parse_args()
    test_corpus(args.corpus_name)

