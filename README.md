# Product Service
## Requirements
 - Python version 3.11
 ## Installation
 The first thing to do is to clone the repository:
 ```sh
 $ git clone https://github.com/erayserter/product-service.git
 $ cd ./product-service
 ```
Create a virtual environment to install dependencies in and activate it:
 ```sh
 $ python3 -m venv venv
 $ source venv/bin/activate
 ```
 Then install the dependencies:
 ```sh
(venv)$ pip install -r requirements.txt
 ``` 
 Make migrations and migrate the database to create tables.
```sh
$ python manage.py makemigrations
$ python manage.py migrate
```
Start the service
```sh
$ python manage.py runserver
```
**Service will be running at** `localhost:8000/`
## Testing
To run tests for modules product and user independently:
```sh
$ MODULE_NAME=product
$ python manage.py test $MODULE_NAME
```
To run all tests:
```sh
$ python manage.py test
```
