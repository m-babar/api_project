# Django Rest API.

It's django project to build django rest API using Django rest framework package.
###### Basically implement Registration, Login, Logout API etc.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites
Python version : python3.6
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

**git clone https://github.com/m-babar/api_project.git**

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
		
		

**Create Playlist API along with assests API docs**

URL : /api/v1/APXPublish/

Endpoints : /APXPublish/
            
Accepted Method : POST

Accepted Method : POST

        Accepted Param in body:
            {
                "Title": "test",
                "Uid": "1dfba3bf-7484-4927-9652-b12154d8b724",
                "assests": [
                    {
                        "Title": "test1",
                        "Uid": "0221db77-11b5-4a33-b7f7-a016860612e6",
                        "Uri": "http://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication",
                        "Type": "TVSHOW"
                    },
                    {
                        "Title": "assest2",
                        "Uid": "dd17b3eb-7c69-4ec3-9573-4d7a5127ab1b",
                        "Uri": "http://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication",
                        "Type": "PROMO"
                    }
                ]
            }

            Accepted success response: 
            {
                "status": 201,
                "message": "Successfully playlist record inserted.",
                "playlist": {
                    "Title": "test",
                    "Uid": "1dfba3bf-7484-4927-9652-b12154d8b724",
                    "Status": "PROCESSING",
                    "CreatedOn": "2018-06-15T11:40:26.310728Z",
                    "CompletedOn": "2018-06-15T11:40:26.310758Z",
                    "Uri": "",
                    "NumberAssets": 2
                }
            } 
            
            
**Retrive Playlist API records**

URL : /api/v1/APXPublish/UID of the playlist/

Endpoints : /APXPublish/1dfba3bf-7484-4927-9652-b12154d8b724/
            
Accepted Method : GET

         
            Accepted success response: 
            {
                "status": 200,
                "message": "Uid related playlist record..",
                "playlist": {
                    "Title": "test",
                    "Uid": "1dfba3bf-7484-4927-9652-b12154d8b724",
                    "Status": "PROCESSING",
                    "CreatedOn": "2018-06-15T11:40:26.310728Z",
                    "ProcessedOn": "2018-06-15T11:40:26.310776Z",
                    "ScheduledOn": "2018-06-15T11:40:26.310789Z",
                    "Duration": "11:40:26.310802",
                    "NumberAssets": 2,
                    "Uri": ""
                }
            }
		
    
**Apply playlist Schedule**
    
URL : /api/v1/APXSchedule/
    
 Endpoints : /APXSchedule/
            
Accepted Method : POST
            

            Accepted Param in body:
            {
                "Title": "fffffff",
                "Uid": "1dfba3bf-7484-4927-9652-b12154d8b724", # playlist UID
                "StartAt": "2018-06-10T01:01",
                "isLoop": false
            }

            Accepted success response: 
            {
                "status": 201,
                "message": "Successfully playlist record inserted.",
                "schedule": {
                    "Title": "fffffff",
                    "Uid": "04e65444-032d-4b3c-a69f-cd6c89e39486",
                    "Status": "PROCESSING",
                    "CreatedOn": "2018-06-15T11:40:26.310728Z",
                    "ProcessedOn": "2018-06-15T11:40:26.310776Z",
                    "ScheduleOn": "2018-06-15T11:40:26.310789Z",
                    "Duration": "11:40:26.310802Z",
                    "Uri": "",
                    "NumberAssets": 2
                }
            }
