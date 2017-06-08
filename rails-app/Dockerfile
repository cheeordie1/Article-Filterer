FROM ruby:2.4.1
RUN apt-get update && apt-get install -qq -y --no-install-recommends \
      build-essential nodejs libpq-dev
RUN mkdir /rails-app
WORKDIR /rails-app
COPY Gemfile Gemfile.lock ./
RUN bundle install
VOLUME /rails-app
