


1 - With Ubuntu 14.04 x64 and logged with standard user with sudo group, can be done like that:
- ```# useradd -m standard``` 
- ```# passwd standard```
- ```# adduser standard sudo```
- ```# su standard```

2 - Logged with standard user and run these command on terminal:
- $ cd ~
- Download zip file 
- $ sudo apt-get -y install unzip
- $ unzip url_shortener.zip

3 - With code extracted, run '$ bash install.sh' script or insert these commands on terminal:
- Update packages repository: 
	$ sudo apt-get update
- Install python: 
	$ sudo apt-get install python-dev
- Install pip to install python packages: 
	$ sudo apt-get -y install python-pip
- Install virtualenvwrapper to create specific packages context: 
	$ sudo pip install virtualenvwrapper
- Add on bashrc: 
	echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc

4 - After, insert these commands on terminal: 
- Sourcing bashrc: 
	$ source ~/.bashrc
- Creating virtual environment dependencies: 
	$ mkvirtualenv url_shortener_env
- Install dependencies for python: 
	$ pip install -e .
- Creating file to database:
	$ touch /tmp/test.db
- Preparing database: 
	$ python prepare_database.py
- Run tests with Python Unit Testing Framework: 
	$ python setup.py test

5 - After, run application with '$ bash start.sh' script or insert these command on terminal:
- $ app

6 - Result:
- Running on http://0.0.0.0:8000/ (Press CTRL+C to quit)
