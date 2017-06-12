import numpy as np
import nltk
import re
import pickle as pkl
import sys

from preprocess import preprocess
from models.model import Model
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import CountVectorizer
from collections import defaultdict
from scipy import spatial

class SIF(Model):
    """
    This class implements the SIF model.  The first section are methods
    to be called in practice for initializing, loading corpuses, and
    highlighting sections of text.
    """
    def __init__(self, a, threshold, mode = 'section', chunk_size = 100):
        """
        Initializes hyper parameters and loads in word embeddings.
        The parameters passed in are as follows:
            - a:           hyperparameter used in the SIF model algorithm
                           for sentence embeddings.
            - threshold:   value that is the minimum similarity to be
                           considered seen by the algorithm
            - mode:        String representing mode.  If section, breaks
                           inputs into chunks.  If sentence, breaks inputs
                           into sentences. If para, breaks inputs into
                           paragraphs.  Default is section
            - chunk_size:  Chunk size for chunk mode.  Default is 100.
        """
        self.a = a
        self.threshold = threshold
        self.chunk_size = chunk_size
        self.total_count = 0
        self.word_counts = defaultdict(int)
        self.sentence_embeddings = None
        self.corpus_sentences = []
        self.mode = mode
        self.default_probability = 1e-2

        # TODO set up a server or database to fetch these from
#        self.word_embeddings = np.load('/home/ubuntu/flask/data/word2vec/word_embedding.npy')
        self.word_embeddings = np.load('data/word2vec/word_embedding.npy')
        #with open('/home/ubuntu/flask/data/word2vec/vocab.pkl', 'rb') as f:
        with open('data/word2vec/vocab.pkl', 'rb') as f:
            self.vocab = pkl.load(f)

    def load_corpus(self, corpus):
        """
        Takes in a corpus represented as a list of articles and 
        adds them to the existing corpus, updating all internal
        variables in the process.
        """
        
        # Compute and update sentence embeddings
        self.word_counts = defaultdict(int)
        self.total_count = 0
        self.corpus_sentences, _ = self.process_articles(corpus, True)
        self.update_unigram_probs()
        self.sentence_embeddings = self.compute_sentence_embeddings(
                                    self.corpus_sentences,
                                    self.a,
                                    self.probabilites)
    
    def highlight(self, article):
        """
        Given an article, returns a list of chunks or sentences
        and a list of their corrosponding similiarites.
        """
        # Some Error Checking and Formatting
        if self.sentence_embeddings is None:
            raise ValueError('No Corpus initialized...')
        
        # Parse article
        sentences, indices = self.process_articles([article], False)
        indices = indices[0]

        # make sentence embeddings and compute similarities
        sent_embeds = self.compute_sentence_embeddings(
                        sentences,
                        self.a,
                        self.probabilites)
        paras, sims = [], []
        assert len(sentences) == len(sent_embeds)
        for i in range(len(sent_embeds)):
            dist = self.compute_similarity(sent_embeds[i])
            paras.append(" ".join(sentences[i]))
            sims.append(dist)
        return indices, sims

    def highlight_corpus(self, corpus):
        """
        Highlights a corpus of articles.
        """
        paras = []
        sims = []
        for article in corpus:
            art_p, art_s = self.highlight(article)
            paras.append(art_p)
            sims.append(art_c)
        return paras, sims, unparsed

    """
    Functions after this are class helper functions.  Generally should
    not be called when using this class.
    """

    def compute_similarity(self, sent):
        """
        Computes the similarity of the closest embedding to the given sentence. 
        """
        return max([((abs(1 - spatial.distance.cosine(sent, embed))))**2
                    for embed in self.sentence_embeddings])

    def compute_sentence_embeddings(self, sentences, a, probabilities):
        """
        Computes the sentence embeddings of given sentences according to
        the SIF model.
        """
        new_embeddings = []
        total_words = 0
        not_in_vocab = 0
        def_prob = 0
        for s in sentences:
            if len(s) == 0:
                continue
            word_calcs = []
            for word in s:
                total_words += 1
                if word in self.vocab:
                    if word.lower() in probabilities:
                        word_calcs.append((a / (a + probabilities[word.lower()]))
                                     * self.word_embeddings[self.vocab[word]])
                    else:
                        def_prob += 1
                        word_calcs.append((a / (a + self.default_probability))
                                    * self.word_embeddings[self.vocab[word]])
                else:
                    not_in_vocab += 1
                    word_calcs.append(np.zeros((300)))
            # NEED A DEFAULT for non-matching words
            vs = np.sum(word_calcs, axis=0) / len(word_calcs)
            new_embeddings.append(vs)
        pca = PCA()
        pca.fit(np.asarray(new_embeddings))
        u = pca.components_[0]
        returned_embeddings = []
        for vs in new_embeddings:
            returned_embeddings.append(vs - vs.dot(u.T) * u)
        return returned_embeddings
    
    def update_unigram_probs(self):
        """
        Calculates unigram probabilites of words in the corpus. 
        """
        self.probabilites = {word : float(self.word_counts[word]) / float(self.total_count)
                             for word in self.word_counts.keys()}

    def split_to_words(self, article):
        """
        This function takes in a string, edits out characters not
        used in calculations, and returns an array of the words.
        """
        char_replace = [',','(',')','"', '/', '.', '?', '!', '[', ']', '{', '}']
        for char in char_replace:
            article = article.replace(char, " ")
        return article.split()

    def chunk_corpus(self, corpus):
        """
        This function takes in a corpus of articles and splits each up
        into chunks of chunk_size.
        """
        new_chunks = []
        for article in corpus:
            split_article = self.split_to_words(article)
            new_chunks += [" ".join(split_article[i:i+self.chunk_size])
                           for i in range(0, len(split_article), self.chunk_size)]
        return new_chunks

    def process_articles(self, corpus, load):
        """
        Takes in a corpus and processes it.  Updates model
        variables if load is set to true.
        """
        chunks = []
        indices = []
        for article in corpus:
            parsed, ind = preprocess(article, self.mode, self.chunk_size)
            for item in parsed:
                if len(item) == 0:
                    continue
                chunks.append(item)
                indices.append(ind)
                if load:
                    self.total_count += len(item)
                    for word in item:
                        self.word_counts[word] += 1
        return chunks, indices
