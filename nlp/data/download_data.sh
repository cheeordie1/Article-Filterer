python3 create_sample_datasets.py
wget http://nlp.stanford.edu/data/glove.840B.300d.zip
unzip glove.840B.300d.zip
rm glove.840B.300d.zip
mv glove.840B.300d.txt word2vec
python3 word2vec/save_word_vecs.py
mv word_vectors* word2vec


