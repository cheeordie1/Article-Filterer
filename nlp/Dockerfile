FROM ubuntu:16.04
RUN apt-get update \
  && apt-get install -y python3-pip python-dev build-essential \
  && pip3 install numpy gensim flask psycopg2 nltk \
  && python3 -m nltk.downloader punkt stopwords
VOLUME /home/ubuntu/flask
CMD "python3 /home/ubuntu/flask/app.py"
