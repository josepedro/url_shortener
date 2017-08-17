sudo apt-get update && 
sudo apt-get -y install python-dev && 
sudo apt-get -y install python-pip && 
sudo pip install virtualenvwrapper && 
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc && 
source ~/.bashrc && 
sudo pip install IPython==5.0 && 
sudo pip install -U pip setuptools && 
sudo apt-get -y install git && 
git clone https://github.com/josepedro/url_shortener.git && 
cd url_shortener && 
mkvirtualenv url_shortener_env && 
pip install -e . && 
python prepare_database.py && 
python setup.py test && 
echo "==== Everything ok! Type sh start.sh to run application. ===="