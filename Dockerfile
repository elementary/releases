FROM jekyll/jekyll:4

# Set default locale for the environment
ENV LC_ALL C.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

COPY Gemfile Gemfile.lock ./
RUN bundle install

ENTRYPOINT ["/usr/local/bin/bundle", "exec", \
  "jekyll", "serve",   \
  "--host", "0.0.0.0", \
  "--port", "4000"]
