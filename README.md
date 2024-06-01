# Instrucoes para WINDOWS!

#
#   PREPARANDO O AMBIENTE
#   https://docs.djangoproject.com/en/5.0/howto/windows/
#

py -m venv EZLunch

EZLunch\Scripts\activate.bat

py -m pip install --upgrade pip

py -m pip install Django

py -m django --version

py -m pip install "colorama >= 0.4.6"

py -m pip install django-debug-toolbar

py -m pip install django-axes

py -m pip install django-dirtyfields

py -m pip install python-decouple


# Para desativar o venv usar:
deactivate

#   EXECUTANDO MIGRATIONS
#   https://docs.djangoproject.com/en/5.0/intro/tutorial02/
#
REMEMBER THE THREE-STEP GUIDE TO MAKING MODEL CHANGES:

Change your models (in models.py).

Run python manage.py makemigrations to create migrations for those changes

Run python manage.py migrate to apply those changes to the database.

py manage.py makemigrations <appName>

py manage.py sqlmigrate <appName> 0001

py manage.py migrate


#   EXECUTANDO O PROJETO
#   Obs: deve estar na pasta que contem o manage.py
#   https://docs.djangoproject.com/en/5.0/intro/tutorial01/
#
py manage.py runserver

# Axes (resetar usuario)
py manage.py axes_reset