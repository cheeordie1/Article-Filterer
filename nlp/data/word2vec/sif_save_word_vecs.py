import numpy as np
import pickle as pkl
from tqdm import tqdm

vec_dim = 300
vocab_size = 2196017

word_embedding = np.zeros((vocab_size, vec_dim))
vocab = {}
with open('word2vec/glove.840B.300d.txt', 'r') as f:
    for i, line in enumerate(tqdm(f, total=vocab_size)):
        l = line.split()
        try:
            word_embedding[i] = [float(num) for num in l[1:]]
        except:
            pass # just skip over vectors which include spaces
        vocab[l[0]] = i

with open('word2vec/vocab.pkl', 'wb') as f:
    pkl.dump(vocab, f)

np.save('word2vec/word_embedding', word_embedding, allow_pickle=False)

    
