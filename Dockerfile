FROM ruby:2.7-buster

# Install program to configure locales as per
# https://github.com/jekyll/jekyll/issues/4268#issuecomment-167406574
RUN apt-get update && apt-get install -y locales
RUN dpkg-reconfigure locales && \
  locale-gen C.UTF-8 && \
  /usr/sbin/update-locale LANG=C.UTF-8

# Install needed default locale for Makefly
RUN echo 'en_US.UTF-8 UTF-8' >> /etc/locale.gen && locale-gen

# Set default locale for the environment
ENV LC_ALL C.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

RUN mkdir -p /opt/io/elementary/releases
WORKDIR /opt/io/elementary/releases

COPY Gemfile ./
RUN gem install jekyll && bundle install

ENTRYPOINT ["/usr/local/bin/bundle", "exec", \
  "jekyll", "serve",   \
  "--host", "0.0.0.0", \
  "--port", "4000"]
