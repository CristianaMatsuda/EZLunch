# Instrucoes para WINDOWS!

<!--
    PREPARANDO O AMBIENTE
    https://docs.djangoproject.com/en/5.0/howto/windows/
-->
py -m venv project-name
project-name\Scripts\activate.bat
py -m pip install --upgrade pip
py -m pip install Django
py -m django --version
py -m pip install "colorama >= 0.4.6"
# Para desativar o venv usar:
deactivate

<!--
    EXECUTANDO O PROJETO
    Obs: deve estar na pasta que contem o manage.py
    https://docs.djangoproject.com/en/5.0/intro/tutorial01/
-->
py manage.py runserver