# Django Rest API.
[![Build Status](https://travis-ci.org/mrakrathod/django-drf-rest-api.png?branch=master)](https://travis-ci.org/mrakrathod/django-drf-rest-api})

It's django project to build django rest API using Django rest framework package.
###### Basically implement Registration, Login, Logout API.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites
Python version : python3.4
###### python installtion in ubuntu machine
**sudo add-apt-repository ppa:jonathonf/python-3.6**
**sudo apt-get update**
**sudo apt-get install python3.6**

**sudo apt-get update**
**sudo apt-get install python3.6**

###### Install virtualenv
**sudo apt-get install python3-pip**
**sudo pip3 install virtualenv**

###### Python installtion in windows machine.
https://www.python.org/downloads/

**Install virtual envoirment**

###### Installing
1. clone from repository

**git clone https://github.com/mrakrathod/django-drf-rest-api.git**

2. create virtualenvoirment

**virtualenv --python=python3.6 drf_env**

3. Activate virtual envoirment

**source drf_env/bin/activate**

4. Install python dependancy packages.
Note, requirments.txt file present in project root direcotry


**pip install -r requirments.txt**

5. start project below command.

**python manage.py runserver**

6. Copy this URL on your browsers tab 

**http://127.0.0.1:8000/**
 
## API endpoints.

**Registration API docs.**

URL : /api/v1/register/

Endpoints : /register/

Accepted Method : POST

            Accepted Param in body:
             {
                "first_name": "",
                "last_name": "",
                "email": "",
                "username": "",
                "user_password": ""
            }

            Accepted success response: 
            {
                "status": 201,
                "message": "Successfully register new user.",
                "token": "ce80f75182ae74bf851d3d7d32941152ed43521e"
            }
			
**Login API docs.**

URL : /api/v1/login/

Endpoints : /login/

Accepted Method : POST

        Accepted Param in body:
        {
            "username": "",
            "password": ""
        }

        Accepted success response: 
        {
            "status": 201,
            "message": "Successfully register new user.",
        }
		

**Logout API docs**

URL : /api/v1/logout/

Endpoints : /logout/

Accepted Method : POST

        Accepted Param in body:
        {
            "token": ""
        }

        Accepted success response: 
        {
            "status": 200,
            "message": "Successfully logout."
        }
		
		
