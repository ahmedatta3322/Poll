
  

# Voting APP

  
  
  

## Installation

  

Install the project with pip , pipenv

  We are Using PIPENV as a package manager

```bash
cd Poll

pip install pipenv

pipenv shell

pipenv install

Python manage.py migrate

Python manage.py runserver
```

  

Then you will need to create your .env

file inside voting directory

  

## example of .env file

    SECRET_KEY = django-insecure-!s$hfsq)5vjh8hx@h$ej&5@@$_r$bj7p)2%(qqmxo@tb$s8kn6

    ACCESS_EXPIRES_IN =  600

    REFRESH_EXPIRES_IN =  3600

 - You can set Access expiry time through .env
 - You can set Refresh expiry time through .env
