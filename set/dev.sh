#!/bin/bash
#
# Script to set project aliases
#

CODE_DIR = ~/fyp/set/code/Python/
FYP_VIRTUALENV = ~/fyp/set/code/Python/fyp_virtualenv/

cd $CODE_DIR
if [ ! -d "$FYP_VIRTUALENV" ]; then
	virtualenv fyp_virtualenv
fi

cd $FYP_VIRTUALENV
sudo source bin/activate

cd /usr/share/setoolkit/

echo "To copy code from python scripts to /usr/share/setoolkit (from $HOME/set/code/Python), press 'y'. Otherwise press another key.";
read option

if [ "$option" = 'y' ]; then
sudo cp $CODE_DIR/*.py /usr/share/setoolkit
fi

echo "To perform packet capture, press 'y'. Otherwise press another key.";
read option

if [ "$option" = 'y' ]; then
gnome-terminal -e 'sudo python /usr/share/setoolkit/packetcapture.py'
fi

sudo python /usr/share/setoolkit/startTool.py

cd $FYP_VIRTUALENV
sudo source bin/deactivate