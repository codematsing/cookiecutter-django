# {{cookiecutter.project_name}}

{{ cookiecutter.description }}

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

{%- if cookiecutter.open_source_license != "Not open source" %}

License: {{cookiecutter.open_source_license}}
{%- endif %}

# Custom Set-up

## Project Preparations:

* Contracts Detail Form:
  * Ask for Personal Information
  * Valid ID
    * ID No
    * Date / Place Issued
  * TIN
  * PhilHealth Number
  * Bank Details
    * Savings Account
    * Photo of Front Face
  * CV
  * Github details
  * Pubkeys
  * SMTP Settings
* Request for dev server credentials
* Request for VPN
* [Handbook Template](./docs/Software%20Development%20Handbook%20Template.docx)

## Step 1: Github
```shell
git clone <project repository>
```

## Step 2: Preparing Dependencies

### Local Development

* When creating virtual environment in local development

```shell
cd <project>

# Script to create virtualenv and automate setting and unsetting of environments in existing environment 
# Dependency: virtualenv
.envs/./initialize_local_venv.sh 
```

* Activating virtual environment

```shell
# Enter virtual environment. 
# This should automatically export env variables in .envs/*
source .local_venv/bin/activate
```

* Installing dependencies

```shell
# Includes base.txt and local.txt dependencies
pip install -r requirements/local.txt
```

* Deactivate virtual environment

```shell
# This should automatically unset env variables in .envs/*
deactivate
```

### Production Deployment

You can use `.prod_venv` as virtual environment for deployment in scratch. Separating virtualenvs for local and production and reduce conflicts of dependencies in case server will tested both local and production settings

* Scratch Deployment

    * Dependencies

    ```shell
    #script to create virtualenv and automate exporting of environments in existing environment
    #dependency, virtualenv .envs/./initialize_prod_venv.sh 

    source .prod_venv/bin/activate

    # For production environment dependencies
    # Includes base.txt and production.txt dependencies
    pip install -r requirements/production.txt
    ```

    * Settings.py: Don't forget to replace settings in `manage.py` to production settings

    * Collectstatic is important during deployment

* Containerized deployment
    * Read [docs](https://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html) for guide

## Step 3: Running the App

* Checking for errors

``` shell
python manage.py check
```

* Migrations

``` shell
python manage.py migrate
```

* Running Server

``` shell
python manage.py runserver
```

## Step 4: Git Branch Standard

[Reference](https://towardsdatascience.com/how-to-structure-your-git-branching-strategy-by-a-data-engineer-45ff96857bb)
![Git Branch Image](https://miro.medium.com/max/786/1*q_w5pcaH7WT1larRd631jQ.webp)

# Additional Standard Practices

* Database should not be containerized and be in separate server
* For Containers:
    * For local deployment, best practice is to mount volume of app to accommodate dynamically changing source code. Do not convert to image.
    * Persistent storage (a.k.a media files) should not be in container. Common practice is to mount volume and link to media directory (follow the settings configuration. Find: "MEDIA_ROOT")

# Common issues during development

Kindly update and/or check [Issues Tracker](./docs/IssuesTracker.md) for any probably issues encountered relating migrations, environment setup, runserver, etc, that could affect other local development environments

* [Need to completely reset database in local development](https://www.linkedin.com/pulse/how-do-i-reset-django-migration-nitin-raturi?trk=pulse-article_more-articles_related-content-card#:~:text=Django%27s%20migration%20can%20be%20reset,and%20python%20manage.py%20migrate.)

```shell
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
# delete and create database
```

Error:
```
django.db.migrations.exceptions.NodeNotFoundError: Migration socialaccount.0001_initial dependencies reference nonexistent parent node ('sites', '0001_initial')

```

Solution:
``` python
# at settings.py
MIGRATION_MODULES = {"sites": "<app_name>.contrib.sites.migrations"} #comment out
```

# Cookiecutter README.md Section

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

-   To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

-   To create a **superuser account**, use this command:

        $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy {{cookiecutter.project_slug}}

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

{%- if cookiecutter.use_celery == "y" %}

### Celery

This app comes with Celery.

To run a celery worker:

``` bash
cd {{cookiecutter.project_slug}}
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.

{%- endif %}
{%- if cookiecutter.use_mailhog == "y" %}

### Email Server

{%- if cookiecutter.use_docker == "y" %}

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server [MailHog](https://github.com/mailhog/MailHog) with a web interface is available as docker container.

Container mailhog will start automatically when you will run all docker containers.
Please check [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html) for more details how to start all containers.

With MailHog running, to view messages that are sent by your application, open your browser and go to `http://127.0.0.1:8025`
{%- else %}

In development, it is often nice to be able to see emails that are being sent from your application. If you choose to use [MailHog](https://github.com/mailhog/MailHog) when generating the project a local SMTP server with a web interface will be available.

1.  [Download the latest MailHog release](https://github.com/mailhog/MailHog/releases) for your OS.

2.  Rename the build to `MailHog`.

3.  Copy the file to the project root.

4.  Make it executable:

        $ chmod +x MailHog

5.  Spin up another terminal window and start it there:

        ./MailHog

6.  Check out <http://127.0.0.1:8025/> to see how it goes.

Now you have your own mail server running locally, ready to receive whatever you send it.

{%- endif %}

{%- endif %}
{%- if cookiecutter.use_sentry == "y" %}

### Sentry

Sentry is an error logging aggregator service. You can sign up for a free account at <https://sentry.io/signup/?code=cookiecutter> or download and host it yourself.
The system is set up with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.
{%- endif %}

## Deployment

The following details how to deploy this application.
{%- if cookiecutter.use_heroku.lower() == "y" %}

### Heroku

See detailed [cookiecutter-django Heroku documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html).

{%- endif %}
{%- if cookiecutter.use_docker.lower() == "y" %}

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).

{%- endif %}
{%- if cookiecutter.frontend_pipeline == 'Gulp' %}
### Custom Bootstrap Compilation

The generated CSS is set up with automatic Bootstrap recompilation with variables of your choice.
Bootstrap v5 is installed using npm and customised by tweaking your variables in `static/sass/custom_bootstrap_vars`.

You can find a list of available variables [in the bootstrap source](https://github.com/twbs/bootstrap/blob/main/scss/_variables.scss), or get explanations on them in the [Bootstrap docs](https://getbootstrap.com/docs/5.1/customize/sass/).

Bootstrap's javascript as well as its dependencies is concatenated into a single file: `static/js/vendors.js`.
{%- endif %}
