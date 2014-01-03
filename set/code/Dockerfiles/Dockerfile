# Python Box
#
# VERSION       1.0

# use the ubuntu base image provided by dotCloud
FROM ubuntu
MAINTAINER Quantza, <post2base@outlook.com>

# make sure the package repository is up to date
run echo "deb http://archive.ubuntu.com/ubuntu precise main universe" > /etc/apt/sources.list

run echo "deb http://archive.scrapy.org/ubuntu precise main" > /etc/apt/sources.list

run curl -s http://archive.scrapy.org/ubuntu/archive.key | apt-key add -

run	apt-get update
run	apt-get upgrade -y

run	apt-get install -y -q curl
run	apt-get install -y -q wget
run	apt-get install -y -q git
run	apt-get install -y -q mercurial
run	apt-get install -y -q build-essential libsqlite3-dev

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
run pip install virtualenv
run	apt-get install -y -q python-dev
run	apt-get install -y -q libxml2-dev libxslt-dev
run	apt-get install -y -q scrapy-0.18

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

##MIGHT NEED TO REMOVE LATER, SINCE NOT IN USE YET
# Install numpy
run 	apt-get install -y -q python-numpy

#Install libsvm
run 	git clone git@github.com:cjlin1/libsvm.git ~/tmp/libsvm/
run 	cd ~/tmp/libsvm/

#Compile libsvm - Might use /usr/local/ instead...
run 	mkdir ~/optbin
run 	./configure --prefix=$HOME/optbin && make && make install

#Install metasploit - Source: http://samiux.blogspot.co.uk/2013/05/howto-metasploit-on-ubuntu-desktop-1204.html
run 	mkdir ~/metasploitInstaller && cd ~/metasploitInstaller

run 	apt-get install -y -q ruby1.9.1 build-essential
run 	wget http://downloads.metasploit.com/data/releases/metasploit-latest-linux-x64-installer.run

run 	chmod +x metasploit-latest-linux-x64-installer.run
run 	./metasploit-latest-linux-x64-installer.run --mode unattended

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
run 	cp ~/fyp/set/dev.sh ~
run     cd ~/fyp/set/code/Python/MainProgram/libsvm/python/
run     make
run     cd ~
run 	chmod +x dev.sh

#Configure and install mail server - dovecot and postfix
run	 apt-get install -y -q dovecot-imapd
run	 useradd --shell /usr/sbin/nologin set_mail

run	 touch /var/log/dovecot.log && touch /var/log/dovecot-info.log
run	 chown set_mail:set_mail /var/log/dovecot.log
run	 chown set_mail:set_mail /var/log/dovecot-info.log
 
run echo "catchall: set_mail" > /etc/aliases
run  cp ~/fyp/set/code/Postfix/main.cf /etc/postfix/

run	 cp ~/fyp/set/code/Dovecot/dovecot.conf /etc/dovecot/
run	 cp ~/fyp/set/code/Dovecot/passwd /etc/dovecot/
run	 service start dovecot

#run code
run 	cd ~ && ./dev.sh

