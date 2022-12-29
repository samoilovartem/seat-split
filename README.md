# Accounts-cards django project documentation


### Deployment algorithm

1. Add Config vars in Heroku app:
* `DJANGO_SETTINGS_MODULE=mysite.settings`
* `SECRET_KEY=our_secret_key`
* `DEBUG=False`
2. Make sure to add everything we don't want to be uploaded in `.gitignore` and run: `git add .`
3. Add your commit: `git commit -m 'your commit'`
4. Push files to Heroku: `git push heroku main`
5. If you encounter problems with Django collectstatic, please run `heroku config:set DISABLE_COLLECTSTATIC=1`and push everything again. Full guide is [here](https://stackoverflow.com/questions/55330749/error-while-running-python-manage-py-collectstatic-noinput-after-changin) for your reference. 


### Tests:
We have multiple tests (CRUD) for these categories:
1. Users
2. Groups
3. Accounts
4. Cards

All tests are tagged by its own category to be able to run them separately. For example this command will run all tests tagged as "users":\
`python manage.py test --tag=users`

In order to speed up all tests we can use threads:\
`python manage.py test --parallel`


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
11. If you ever you deleted [Django migrations](https://stackoverflow.com/questions/37603203/django-deleted-migrations-directory)
12. Git Cheat [Sheet](http://res.cloudinary.com/hy4kyit2a/image/upload/SF_git_cheatsheet.pdf)
13. JWT [decoding](https://jwt.io/)
14. Using [dictionary](https://stackoverflow.com/questions/72623440/django-name-filter-name-icontains-is-not-defined) as filter value
15. Super useful approaches of how to get user and group permissions is [here](https://stackoverflow.com/questions/16573174/how-to-get-user-permissions)


#### Useful commands:
1. Access project's bash:\
`heroku run bash -a <heroku app name>`
2. Check all releases:\
`heroku releases`
3. Check all info about particular release:\
`heroku releases:info <release version number>`
4. If ever we deployed buggy code or something goes wrong with current release:\
`git revert`and redeploy it again.
5. If we have some problems with heroku platform, then better to use:\
`heroku rollback <release version number (optional)>`
6. Heroku app logs:\
`heroku logs -n 1500`or `heroku logs -t`to maintain them live
7. Safely delete all rows from database:\
`python manage.py truncate --apps <app_name> --models <model_name>`
8. Reset PK in postgresql DB (apply only after deleting all info from the table):\
`python manage.py sqlsequencereset <app_name> | python manage.py dbshell`
9. Safely delete an app:\
`python manage.py migrate <app_name> zero`\
After running this command we can delete an app from INSTALLED_APPS and delete a corresponding directory
10. Automatically upgrade all requirements:\
`pur -r requirements.txt`