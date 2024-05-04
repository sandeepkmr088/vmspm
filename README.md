# Django Developer Assignment
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

## cd vms
(env)  $ cd vms

## Database using MySQL so install mysqlclient
(env) $ vms> pip install mysqlclient

## Then create migration file
(env) $ vms> python manage.py makemigrations

## Then create database
(env) $ vms> python manage.py migrate

## Then create superuser
(env) $ vms> python manage.py createsuperuser

## Create app name core
(env) $ vms> django-admin startapp core


