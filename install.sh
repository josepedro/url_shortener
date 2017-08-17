#!/usr/bin/env 

sudo apt-get update && 
sudo apt-get -y install python-dev && 
sudo apt-get -y install python-pip && 
sudo pip install virtualenvwrapper && 
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc && 
echo "==== Everything ok! Continue with procedures number 4 on terminal. ===="
