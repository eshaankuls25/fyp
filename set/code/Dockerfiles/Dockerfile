# Python Box
#
# VERSION       1.0

# use the ubuntu base image provided by dotCloud
FROM ubuntu
MAINTAINER Quantza, <post2base@outlook.com>

# make sure the package repository is up to date
run echo "deb http://archive.ubuntu.com/ubuntu precise main universe" > /etc/apt/sources.list

run 	apt-get update
run 	apt-get upgrade -y

run	apt-get install -y -q curl
run	apt-get install -y -q wget
run	apt-get install -y -q git
run	apt-get install -y -q mercurial
run 	apt-get install -y -q build-essential libsqlite3-dev

#Expose http port (80)
EXPOSE 	80

#Install useful apps
run 	apt-get install -y -q memcached
run 	apt-get install -y -q python

#add readline support
run 	apt-get install -y -q rlwrap

#Install python
run	apt-get install -y -q python-pip
run	pip install s3cmd
run	pip install python-magic

# Runtime dependencies
run	apt-get install -y -q iptables
run	apt-get install -y -q lxc
run	apt-get install -y -q aufs-tools

# Install impacket
#run 	mkdir ~/impacket
#run 	cd ~/impacket
#run 	wget https://impacket.googlecode.com/files/impacket-0.9.10.tar.gz
#run 	tar -xzvf *.tar.gz
#run 	cd impacket* && python setup.py install

# Install pcapy
run 	apt-get install -y -q python-pcapy

#Install metasploit - Source: http://samiux.blogspot.co.uk/2013/05/howto-metasploit-on-ubuntu-desktop-1204.html
run 	mkdir ~/metasploitInstaller && cd ~/metasploitInstaller

run 	apt-get install -y -q ruby1.9.1 build-essential
run 	wget http://downloads.metasploit.com/data/releases/metasploit-latest-linux-x64-installer.run

run 	chmod +x metasploit-latest-linux-x64-installer.run
	run sudo ./metasploit-latest-linux-x64-installer.run --mode unattended

#Without registering the install, cannot update it! Remember this.
run 	update-rc.d metasploit disable

#Run metasploit
run 	/etc/init.d/metasploit start
#run 	cd /opt/metasploit/app && msfconsole

#Clone and install social-engineer-toolkit
run 	cd ~
run 	git clone https://github.com/trustedsec/social-engineer-toolkit/ set/
run 	cd set && python setup.py install

#Clone fyp repo
run 	git clone https://github.com/Quantza/fyp ~/fyp/
run 	cp ~/fyp/set ~/set
run 	cp ~/set/code/dev.sh ~
run 	chmod +x dev.sh

#run code
run 	cd ~ && ./dev.sh

# git pull and install dotfiles as well
#run 	git clone git@github.com:Quantza/dotfiles.git
#run 	ln -sb dotfiles/.screenrc .
#run 	ln -sb dotfiles/.tmux .
#run 	ln -sb dotfiles/.gitmessage.txt .
#run 	ln -sb dotfiles/.bash_profile .
#run 	ln -sb dotfiles/.bashrc .
#run 	ln -sb dotfiles/.bashrc_custom .
#run 	ln -sf dotfiles/.emacs.d .
#run 	ln -sf dotfiles/.tmux .
#run 	ln -sf dotfiles/.vagrant.d .
