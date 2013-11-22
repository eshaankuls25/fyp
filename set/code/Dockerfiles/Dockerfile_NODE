# Node.js Box
#
# VERSION       1.0

# use the ubuntu base image provided by dotCloud
FROM ubuntu
MAINTAINER Quantza, <post2base@outlook.com>

# make sure the package repository is up to date
RUN echo "deb http://archive.ubuntu.com/ubuntu precise main universe" > /etc/apt/sources.list

RUN apt-get update
RUN apt-get upgrade -y

#Expose http port (80)
EXPOSE 80

#Install useful apps
RUN apt-get install -y memcached
RUN apt-get install -y tmux
RUN apt-get install -y node
RUN apt-get install -y python
RUN apt-get install -y emacs

# Install nvm: node-version manager
# https://github.com/creationix/nvm
RUN apt-get install -y git
RUN apt-get install -y curl
RUN curl https://raw.github.com/creationix/nvm/master/install.sh | sh

# Load nvm and install latest production node
RUN source $HOME/.nvm/nvm.sh
RUN nvm install v0.10.12
RUN nvm use v0.10.12

# Install jshint to allow checking of JS code within emacs
# http://jshint.com/
RUN npm install -g jshint

# Install rlwrap to provide libreadline features with node
# See: http://nodejs.org/api/repl.html#repl_repl
RUN apt-get install -y rlwrap

# Install emacs24
# https://launchpad.net/~cassou/+archive/emacs
RUN add-apt-repository -y ppa:cassou/emacs
RUN apt-get -qq update
RUN apt-get install -y emacs24-nox emacs24-el emacs24-common-non-dfsg

# Install Heroku toolbelt
# https://toolbelt.heroku.com/debian
RUN wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh

#Install restler, cheerio and commander
RUN npm install -g express
RUN npm install restler
RUN npm install commander
RUN npm install cheerio

# git pull and install dotfiles as well
RUN git clone git@github.com:Quantza/dotfiles.git
RUN ln -sb dotfiles/.screenrc .
RUN ln -sb dotfiles/.tmux .
RUN ln -sb dotfiles/.gitmessage.txt .
RUN ln -sb dotfiles/.bash_profile .
RUN ln -sb dotfiles/.bashrc .
RUN ln -sb dotfiles/.bashrc_custom .
RUN ln -sf dotfiles/.emacs.d .
RUN ln -sf dotfiles/.tmux .
RUN ln -sf dotfiles/.vagrant.d .
