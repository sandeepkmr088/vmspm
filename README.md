# Djangorestframework Project 
## Vendor Management System with Performance Metrics
## Objective:
Develop a Vendor Management System using Django and Django REST Framework. This
system will handle vendor profiles, track purchase orders, and calculate vendor performance
metrics.

## Make directory using command
$ mkdir vmspm

## Install virtualenv inside vmspm directory
$ pip install virtualenv

## Create virtualenv inside this folder
$ python -m venv env 

## Then Activate the virtualenv
##### $ .\env\Scripts\activate   -----> for Window
##### $  source env/bin/activate  ----> for Linux

## Install django and restframework 
(env) $ pip install django , (env)  $ pip install djangorestframework

## Create django project 
(env)  $ django-admin startproject vms

## Change diectory to vms
(env)  $ cd vms

## MySQL database used so install mysqlclient
(env) $ vms> pip install mysqlclient

## Then create migration file
(env) $ vms> python manage.py makemigrations

## Then create tables in database
(env) $ vms> python manage.py migrate

## Then create superuser
(env) $ vms> python manage.py createsuperuser

## Create app name core
(env) $ vms> django-admin startapp core  or python .\manage.py startapp core

## Add 'rest_framewrok' and 'core' inside INSTALLED_APPS in  settings.py
## Then Create Models in core/models.py ----> serializers in core/serializer.py ------> view in core/views.py -------->  urls in core/urls.py
## Also do change in vms/urls.py

## Run makemigrations and migrate command

## Finally run django application
(env) $ vms> python manage.py runserver

## Open in any browser http://localhost:8000/api/vendors/ ,http://localhost:8000/api/vendors/1/ , http://localhost:8000/api/vendors/, http://localhost:8000/api/purchase_orders/, http://localhost:8000/api/purchase_orders/1/




