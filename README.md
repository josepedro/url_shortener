# URL Shortener

This application is a URL Shortener API RESTful service.

## Directory Structure

```GAP
├─ app/ 	# All application code in this directory.
│  ├─ tests/    
│  │  └─ test_url_shortener.py 	# Several tests by using Python Unit Testing Framework. 
│  └─ url_shortener/
│     └─ url_shortener.py 	# Model, View, Controller and Schemas of database.
├─ app.egg-info/ 	# Configurations file of python library setuptools.
├─ install.sh 	# Script bash to install dependencies.
├─ prepare_database.py 	# Script to create database and tables by using SQLite. 
├─ README.md 	# Informations and instructions.
├─ setup.py 	# Script to configure and execute python application.
└─ start.sh 	# Script bash to run application.
```
## Architecture

This application was build by using microframework for Python Flask.
Module url_shortener.py have MVC pattern implemented.
There are two Model classes: User and Url.
These classes were implemented by using agregation one to many, i.e., User have many Urls.
All functions was tested by using Python Unit Testing Framework.

## Instructions

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
	$ echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc

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
