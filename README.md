# Instrucoes para WINDOWS!

#
#   PREPARANDO O AMBIENTE
#   https://docs.djangoproject.com/en/5.0/howto/windows/
#

py -m venv EZLunch

EZLunch\Scripts\activate.bat

py -m pip install --upgrade pip

pip install -r requirements.txt

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


# Alterar models do axes
class AccessLog(AccessBase):
    logout_time = models.DateTimeField(_("Logout Time"), null=True, blank=True)

    def __str__(self):
        return f"Access Log for {self.username} @ {self.attempt_time}"

    @property
    def uptime(self):
        from datetime import timedelta
        if self.logout_time:
            return self.logout_time - self.attempt_time
        return timedelta(0)

    class Meta:
        verbose_name = _("access log")
        verbose_name_plural = _("access logs")