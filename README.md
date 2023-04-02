# CRM django backend documentation

### Description:

This project is a CRM Django backend that provides API endpoints and functionalities for managing users, groups, accounts, cards and mobile transactions. It uses Django as the framework, Django Rest Framework for API creation, and Simple JWT for authentication.

### Installation:

1. Clone the repository from GitHub.
2. Create `.env.prod` and `.env.dev` in django-backend directory using `.env.prod.example` and `.env.dev.example`.
3. Install Docker and launch the daemon.
4. Cd to project's root and run `docker compose up`.

### Project structure:
#### Directories:

- **django-backend** - contains all necessary files for Django backend.
  - **apps** - contains all existing django applications and common (among them) files.
  - **config** - contains standard Django settings files.
  - **static** - contains static files of all django custom apps, standard apps and installed libraries (not available in git repository).
  - **templates** - contains Django admin template settings.
- **instruction_files** - contains a simple. instruction for using admin panel and all necessary screenshots.
- **migration_manager** - contains all necessary `.py` files for cleaning data and preparing it for migration from CSV to Postgresql using Django admin panel.
- **nginx** - contains all necessary files for nginx configuration.
- **shell_scripts** - contains all shell commands that can make our life much easier.
   - **create_requirements.sh** - creates `dev-requirements.txt` and `prod-requirements.txt` files.
   - **docker_deploy.sh** - builds docker container and pushes it to Heroku.
   - **run_tests.sh** - runs all tests and creates html report.
   - **make_project_structure.sh** - creates project structure.
   - **heroku_backup.sh** - contains all necessary commands to backup Heroku database.
   - **count_lines_of_code.sh** - counts all lines of code in the project.


#### Separated files:

- **.dockerignore** - list of files or directories that are excluded from getting into docker container.
- **.flake8** - custom settings for flake8 linter.
- **.gitignore** - list of files or directories that are excluded from getting into git repository.
- **.pre-commit-config.yaml** - custom settings for flake8, black and isort linters hooks.
- **docker-compose.yml** - file-constructor, that allows to build docker container. Used for local development only.
- **Dockerfile** - file-instruction of how to build docker image for Heroku deployment. Used for production on Heroku only.
- **Dockerfile-dev** - file-instruction of how to build docker image for local development. This is the file, that `docker-compose.yml` is using for building docker container to run it locally.
- **Dockerfile-prod** - file-instruction of how to build docker image for production deployment. Used for production only.
- **pyproject.toml** - custom project's settings. This file contains all necessary information about the project itself, dev and prod dependencies. Used to create `dev-requirements.txt` and `prod-requirements.txt` files.

### Deployment to Heroku
#### Using git (not recommended):

1. Add Config vars in Heroku app:
   * `DJANGO_SETTINGS_MODULE=mysite.settings`
   * `SECRET_KEY=our_secret_key`
   * `DEBUG=False`
2. Make sure to add everything we don't want to be uploaded in `.gitignore` and run: `git add .`
3. Add your commit: `git commit -m 'your commit'`
4. Push files to Heroku: `git push heroku main`
5. If you encounter problems with Django collectstatic, please run `heroku config:set DISABLE_COLLECTSTATIC=1`and push everything again. Full guide is [here](https://stackoverflow.com/questions/55330749/error-while-running-python-manage-py-collectstatic-noinput-after-changin) for your reference.

#### Using Container Registry (preferred):

1. Prepare correct Dockerfile
2. Use this command to build the container:\
`docker build -t registry.heroku.com/<app_name>/web .`
3. Push the container to registry.heroku.com:\
`docker push registry.heroku.com/<app_name>/web`
4. Release the container to production:\
`heroku container:release -a <app_name> web`

Also, you can simply run `docker_deploy.sh`and script will complete these 3 commands for you.

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

Though the better way to run tests is to use `coverage` package, which is already installed (check requirements.txt).

To get full detailed report with html output use this command:\
`coverage run manage.py test -v 2 && coverage report && coverage html`

HTML report can be viewed in **_htmlcov/index.html_**

Also, you can simply run `run_tests.sh`and choose from provided options.


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
11. Check project's files with flake8 and black before making commit:\
`pre-commit run --all-files`
