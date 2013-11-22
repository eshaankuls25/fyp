#!/bin/bash
#
# Script to set project aliases
#

cd /usr/share/setoolkit/

echo "To copy code from python scripts to /usr/share/setoolkit (from $HOME/set/code/Python), press 'y'. Otherwise press another key.";
read option

if [ "$option" = 'y' ]; then
sudo cp ~/set/code/Python/*.py /usr/share/setoolkit
fi

gnome-terminal -e 'sudo python /usr/share/setoolkit/packetcapture.py'
sudo python /usr/share/setoolkit/startTool.py
