FROM ubuntu:16.04
RUN apt-get update \
  && apt-get install -y python3-pip python-dev build-essential \
  && apt-get install -y libxml2-dev libxslt-dev \
  && apt-get install -y libjpeg-dev zlib1g-dev libpng12-dev \
  && pip3 install newspaper3k flask
VOLUME /home/ubuntu/flask
CMD "python3 /home/ubuntu/flask/app.py"
