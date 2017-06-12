import nltk
import sys
import re

MIN_SECTION_LENGTH = 50

def compute_indices(chunks, mode):
    indices = [(0, len(chunks[0])+2)]
    for c in chunks[1:]:
        last_end = indices[-1][1]
        if mode == 'sentence':
            indices.append((last_end, last_end + len(c) + 1))
        else:
            indices.append((last_end, last_end + len(c) + 2))
    return indices
    
# takes a string of text
def tokenize(string):
    return [w.lower() for w in nltk.tokenize.word_tokenize(string)  \
            if w not in nltk.corpus.stopwords.words('english')]

"""Takes in an article string and gives back tokenized lists of words
   Split into sentences, paragraphs or sections based on mode param
   For the section mode one can also provide a minimum section length
   All sections are padded out to full paragraphs
   Modes:
       'sentence'
       'para'
       'section'
"""
def preprocess(article, mode='section', min_section_length=100):
    if mode == 'sentence':
        sens = article.split('.')
        indices = compute_indices(sens, mode)
        sens = [tokenize(s) for s in sens]
        return sens, indices

    elif mode == 'para':
        paras = article.split('\n\n')
        indices = compute_indices(paras, mode)
        paras = [tokenize(s) for s in paras]
        return paras, indices

    elif mode == 'section':
        paras = article.split('\n\n')
        indices = compute_indices(paras, mode)
        paras = [tokenize(s) for s in paras]
        cur_len = 0
        cur_paras = []
        cur_ind = 0
        inds = []
        sections = []
        for i, para in enumerate(paras):
            cur_len += len(para)
            cur_paras += para
            if cur_len >= min_section_length:
                cur_len = 0
                sections.append(cur_paras)
                inds.append((indices[cur_ind][0], indices[i][1]))
                cur_ind = i+1
                cur_paras = []
            else:
                # preserve paragraph in output
                cur_paras += ['\n\n']
        sections.append(cur_paras[:-1])
        inds.append((indices[cur_ind][0], indices[i][1]))
        return sections, inds
    else:
        raise Exception('Please pass in a valid mode: \nsentence \npara \nsection')

# test
if __name__ == '__main__':
    test_str = 'The success of neural network methods for computing word embeddings has motivated \
            methods for generating semantic embeddings of longer pieces of text, such \
            as sentences and paragraphs. Surprisingly, Wieting et al (ICLR’16) showed that \
            such complicated methods are outperformed, especially in out-of-domain (transfer \
                learning) settings, by simpler methods involving mild retraining of word embeddings \
            and basic linear regression. The method of Wieting et al. requires retraining \
            with a substantial labeled dataset such as Paraphrase Database (Ganitkevitch et \
                al., 2013). \n\n \
            The current paper goes further, showing that the following completely unsupervised \
            sentence embedding is a formidable baseline: Use word embeddings computed \
            using one of the popular methods on unlabeled corpus like Wikipedia, represent \
            the sentence by a weighted average of the word vectors, and then modify \
            them a bit using PCA/SVD. This weighting improves performance by about 10% \
            to 30% in textual similarity tasks, and beats sophisticated supervised methods including \
            RNN’s and LSTM’s. It even improves Wieting et al.’s embeddings. This \
            simple method should be used as the baseline to beat in future, especially when \
            labeled training data is scarce or nonexistent. \n\n \
            The paper also gives a theoretical explanation of the success of the above unsupervised \
            method using a latent variable generative model for sentences, which is \
            a simple extension of the model in Arora et al. (TACL’16) with new “smoothing” \
            terms that allow for words occurring out of context, as well as high probabilities \
            for words like and, not in all contexts.'
    pp = preprocess(test_str, mode='section', min_section_length=50)

    print(len(pp))
    print(pp)

        
    
