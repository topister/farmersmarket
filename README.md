# farmersmarket

## Getting started
Install python3 

Ensure you have pip3 installed sudo apt-get install python3-pip

Ensure you have virtualenv installed sudo apt-get install python3-pip

Create virtual environment virtualenv -p python3 myenv

Activate virtual environment source venv/bin/activate

Clone repo git clone https://github.com/topister/farmersmarket.git

Move to emarketproject directory cd emarketproject

Install dependencies pip3 install -r requirements.txt

Make migrations to avoid foreign key problems python manage.py makemigrations users

Migrate migrations python manage.py migrate

Start server python manage.py runserver

Go to the link http://127.0.0.1:8000/

## How to use
Create superuser from terminal python manage.py createsuperuser

Enter email and password

Go to admin page http://127.0.0.1:8000/admin

Start by admin product, category, farmers, experts, blogs, etc

Add product and select its category

Go to http://127.0.0.1:8000/ and see results

## Technologies used
HTML5

CSS3

JavaScript

Bootstrap

Python

Django

