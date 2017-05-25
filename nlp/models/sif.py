import numpy as np
import nltk
import re
import pickle

from models.model import Model
from sklearn.decomposition import PCA
from collections import defaultdict

EMBED_PATH = 'data/word2vec/word_vectors'

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


class SIF(Model):
    def __init__(self, alpha, beta, a, threshold):
        # Hyper parameters for SIF model
        self.alpha = alpha
        self.beta = beta
        self.a = a
        self.threshold = threshold
        with open(EMBED_PATH, 'rt') as f:
            data = f.readlines()
        info = data[0].split()
        #vocab_len = float(info[0])
        #dims = float(info[1])
        self.word_embeddings = {}
        for line in data[1:]:
            entry = line.split()
            if isfloat(entry[1]):
                self.word_embeddings[entry[0]] = np.array([float(num) for num in entry[1:]])
        pickle.dump(self.word_embeddings, open("word_embeddings.txt", "wb"))

    def load_corpus(self, corpus):
        # First compute all unigram probabilites
        all_words = [word.lower() for article in corpus
                                  for word in nltk.tokenize.word_tokenize(article)]
        self.probabilites = self.compute_unigram_probs(all_words)
        
        # Compute Sentence embeddings
        sentences = [sent for article in corpus
                    for sent in nltk.tokenize.sent_tokenize(article)]
        self.sentence_embeddings = self.compute_sentence_embeddings(
                                    self.word_embeddings,
                                    sentences,
                                    self.a,
                                    self.probabilites)

    def highlight(self, article):
        sentences = [sent for sent in nltk.tokenize.sent_tokenize(article)]
        sent_embeds = self.compute_sentence_embeddings(
                        self.word_embeddings,
                        sentences,
                        self.a,
                        self.probabilites)
        for i in range(len(sent_embeds)):
            dist = self.compute_min_dist(sent_embeds[i])
            if dist < self.threshold:
                print(senctences[i])

    def compute_min_dist(sent):
        return min([abs(np.sum(sent - embed)) for embed in self.sentence_embeddings])

    def compute_sentence_embeddings(self, words, sentences, a, probabilities):
        # Shape??
        new_embeddings = []
        for s in sentences:
            word_calcs = []
            for word in s:
                if word in words:
                    word_calcs.append((a / (a + probabilities[word])) * words[word])
            vs = (1 / np.linalg.norm(s)) * np.sum(np.asarray(word_calcs))
            new_embeddings.append(vs)
        pca = PCA()
        pca.fit(np.asarray(new_embeddings))
        u = pca.components_[0]
        returned_embeddings = []
        for vs in new_embeddings:
            returned_embeddings.append(vs - np.matmul(u, np.matmul(u.transpose(), vs)))
        return np.asarray(returned_embeddings)
    
    def compute_unigram_probs(self, corpus):
        total_count = 0
        word_counts = defaultdict(int)
        for word in corpus:
            word_counts[word] += 1
            total_count += 1
        return {word : float(word_counts[word]) / float(total_count)
                for word in word_counts.keys()}

