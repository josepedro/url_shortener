#!/usr/bin/env 

sudo apt-get update && 
sudo apt-get -y install python-dev && 
sudo apt-get -y install python-pip && 
sudo pip install virtualenvwrapper && 
#echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.bashrc &&
#echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc && 
#source ~/.bashrc && 
source /usr/local/bin/virtualenvwrapper.sh
sudo pip install IPython==5.0 && 
sudo pip install -U pip setuptools && 
#sudo apt-get -y install git && 
mkvirtualenv url_shortener_env && 
pip install -e . &&
touch test.db && 
python prepare_database.py && 
python setup.py test && 
echo "==== Everything ok! Type sh start.sh to run application. ===="
