from paver.easy import *
from paver.virtual import virtualenv
import os

@task
@needs('createvenv')
@virtualenv(dir="venv")
def install():
    os.system('pip3 install -r requirements.txt')

@task
def createvenv():
    os.system('pip3 install virtualenv')
    os.system('virtualenv -p python3.6 venv')

@task
@virtualenv(dir="venv")
def bash():
    os.system('echo \'PS1="(venv) \u:\w\$"\' > initfile')
    os.system('. venv/bin/activate; bash --init-file initfile')
    os.system('rm initfile')

@task
@virtualenv(dir="venv")
def migrate():
    os.system('python manage.py migrate')

@task
@needs('migrate')
@virtualenv(dir="venv")
def run():
    os.system('python manage.py runserver 0.0.0.0:8765')
