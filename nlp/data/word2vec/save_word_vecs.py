import re
import sys
import gensim
import smart_open
from gensim.models.keyedvectors import KeyedVectors

def glove2word2vec(glove_vector_file, output_model_file):
    """Convert GloVe vectors into word2vec C format"""

    def get_info(glove_file_name):
        """Return the number of vectors and dimensions in a file in GloVe format."""
        with smart_open.smart_open(glove_file_name) as f:
            num_lines = sum(1 for line in f)
        with smart_open.smart_open(glove_file_name) as f:
            num_dims = len(f.readline().split()) - 1
        return num_lines, num_dims

    def prepend_line(infile, outfile, line):
        """
        Function to prepend lines using smart_open
        """
        with smart_open.smart_open(infile, 'r') as old:
            with smart_open.smart_open(outfile, 'w') as new:
                new.write(str(line.strip()) + "\n")
                for line in old:
                    new.write(line)
        return outfile

    num_lines, dims = get_info(glove_vector_file)

    gensim_first_line = "{} {}".format(num_lines, dims)
    model_file = prepend_line(glove_vector_file, output_model_file, gensim_first_line)


    print("loading word2vec")
    # Demo: Loads the newly created glove_model.txt into gensim API.
    word_vectors = KeyedVectors.load_word2vec_format(model_file, binary=False) #GloVe Model
    word_vectors.save('word_vectors.out')

    return model_file

glove2word2vec('word2vec/glove.840B.300d.txt', 'word2vec/word_vectors')
