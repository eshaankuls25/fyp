# Python Box
#
# VERSION       1.0

# use the ubuntu base image provided by dotCloud
FROM ubuntu
MAINTAINER Quantza, <post2base@outlook.com>

# make sure the package repository is up to date
run echo "deb http://archive.ubuntu.com/ubuntu precise main universe" > /etc/apt/sources.list

run apt-get update
run apt-get upgrade -y

run	apt-get update
run	apt-get install -y -q curl
run	apt-get install -y -q git
run	apt-get install -y -q mercurial
run apt-get install -y -q build-essential libsqlite3-dev

#Expose http port (80)
EXPOSE 80

#Install useful apps
run apt-get install -y memcached
run apt-get install -y tmux
run apt-get install -y python
run apt-get install -y python
run apt-get install -y emacs

# Install git and curl:
run apt-get install -y git
run apt-get install -y curl

# Install rlwrap to provide libreadline features 
run apt-get install -y rlwrap

# Install emacs24
# https://launchpad.net/~cassou/+archive/emacs
run add-apt-repository -y ppa:cassou/emacs
run apt-get -qq update
run apt-get install -y emacs24-nox emacs24-el emacs24-common-non-dfsg

#Install python
run	apt-get install -y -q python-pip
run	pip install s3cmd
run	pip install python-magic

# Runtime dependencies
run	apt-get install -y -q iptables
run	apt-get install -y -q lxc
run	apt-get install -y -q aufs-tools



# git pull and install dotfiles as well
run git clone git@github.com:Quantza/dotfiles.git
run ln -sb dotfiles/.screenrc .
run ln -sb dotfiles/.tmux .
run ln -sb dotfiles/.gitmessage.txt .
run ln -sb dotfiles/.bash_profile .
run ln -sb dotfiles/.bashrc .
run ln -sb dotfiles/.bashrc_custom .
run ln -sf dotfiles/.emacs.d .
run ln -sf dotfiles/.tmux .
run ln -sf dotfiles/.vagrant.d .
