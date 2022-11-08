# Accounts-cards django project documentation


To be continued ...


Take note that there is no familiar `settings.py` file. Instead, we have **_settings_** folder inside **_mysite_** directory, which contains 4 different  files:
1. `common.py` contains almost all settings from familiar `settings.py` file that are needed for both `development.py` and `production.py`
2. `development.py` contains parts of Django settings for development usage only.
3. `production.py`contains parts of Django settings for production usage only (particularly Heroku)
4. `local.py`contains sensitive information like SECRET_KEY (we store it there in order to be able to use Docker, because Docker can't build a container if SECRET_KEY is inside environmental variable) or DB credentials. This file is in `.gitignore`

Also, changes are made in `wsgi.py` and `manage.py`in order to use different settings files instead of just one.

**Our version**:`os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings.development')`

**Standard Django version:**`os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')`


### Deployment algorithm

1. Add Config vars in Heroku app:
* `DJANGO_SETTINGS_MODULE=mysite.settings.development`
* `SECRET_KEY=our_secret_key`
* `DEBUG=False`
2. Make sure to add everything we don't want to be uploaded in `.gitignore` and run: `git add .`
3. Add your commit: `git commit -m 'your commit'`
4. Push files to Heroku: `git push heroku main`
5. If you encounter problems with Django collectstatic, please run `heroku config:set DISABLE_COLLECTSTATIC=1`and push everything again. Full guide is [here](https://stackoverflow.com/questions/55330749/error-while-running-python-manage-py-collectstatic-noinput-after-changin) for your reference. 



#### Useful notes:
1. Heroku `python manage.py collectstatic` issue solution can be found [here](https://stackoverflow.com/questions/55330749/error-while-running-python-manage-py-collectstatic-noinput-after-changin).
2. Django-tabulator-example is [here](https://github.com/cuauhtemoc-amdg/django-tabulator-example).
3. Responsive tables using Django and htmx. The main article is [here](https://enzircle.com/responsive-table-with-django-and-htmx#comments-list). Github [source code](https://github.com/joashxu/dj-htmx-fun). 
4. Django-tables2 [documentation](https://django-tables2.readthedocs.io/en/latest/index.html).
5. Django-filter [documentation](https://django-filter.readthedocs.io/en/stable/index.html).
6. Django-crispy-forms [documentation](https://django-crispy-forms.readthedocs.io/en/latest/index.html).
7. Django Model meta [options](https://docs.djangoproject.com/en/4.1/ref/models/options/).
8. Detailed Django Form [explanation](https://simpleisbetterthancomplex.com/article/2017/08/19/how-to-render-django-form-manually.html).
9. Django Widget Tweaks is [here](https://simpleisbetterthancomplex.com/2015/12/04/package-of-the-week-django-widget-tweaks.html).
10. Django permissions [detailed article](https://dandavies99.github.io/posts/2021/11/django-permissions/).


#### Useful commands:
1. Access project's bash:\
`heroku run bash -a <heroku app name>`
    