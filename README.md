# Releases

See all releases and the status of repos at releases.elementary.io

## Building

You'll need the following dependencies:
```
ruby-full
build-essential
zlib1g-dev
```

We recommend installing gems to a (hidden) directory in your home folder:
```sh-session
$ echo '' >> ~/.bashrc
$ echo '# Install Ruby Gems to ~/.gems' >> ~/.bashrc
$ echo 'export GEM_HOME="$HOME/.gems"' >> ~/.bashrc
$ echo 'export PATH="$HOME/.gems/bin:$PATH"' >> ~/.bashrc
$ echo '' >> ~/.bashrc
$ source ~/.bashrc
```

Install jekyll and bundler:
```sh-session
$ gem install jekyll bundler
```

Install gems:
```sh-session
$ bundle install
```

Build and serve locally with:
```sh-session
$ bundle exec jekyll serve --host 0.0.0.0
```

The site should now be available at http://0.0.0.0:4000/ on your local machine, and your local machine's IP address on your network—great for testing on mobile OSes.

### Alternative: building with Docker

You'll need Docker installed on your system.

Build the Docker image:
```sh-session
$ bin/build-container
```

Build and serve locally with:
```sh-session
$ bin/serve
```

The site should now be available at http://0.0.0.0:4000/
