# Set-up

## Step 1: Github
```shell
git clone <project repository>
```

```shell
# whenever pulling repository for update this will ensure that submodules are synced
git pull --recurse-submodules
```

## Step 2: Preparing Dependencies

### Local Development

* Activating virtual environment

```shell
# enter virtual environment. 
# this should automatically export env variables in .envs/*
source .local_venv/bin/activate
```

* Installing dependencies

```shell
# Includes base.txt and local.txt dependencies
pip install -r requirements/local.txt
```

* Deactivate virtual environment

```shell
# this should automatically unset env variables in .envs/*
deactivate
```

### Production Deployment

You can use `.prod_venv` as virtual environment for deployment in scratch and to separate dependencies from `.local_venv` in case server will be tested both local and production settings

* Scratch Deployment

```shell
# For production environment dependencies
# Includes base.txt and production.txt dependencies
pip install -r requirements/production.txt
```

* Containerized deployment
    * read [docs](https://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html)
    
## Step 3: Adding new apps

``` shell
cookiecutter ../utils/cookiecutter-app
```

## Step 4: Git Branch Standard

[Reference](https://towardsdatascience.com/how-to-structure-your-git-branching-strategy-by-a-data-engineer-45ff96857bb)

![Git Branch Image](https://miro.medium.com/max/786/1*q_w5pcaH7WT1larRd631jQ.webp)

# Viewing Base Documentation

* After you have set up to develop locally, run the following command from the project directory to build and serve HTML documentation:

```shell
make -C docs livehtml
```

* If you set up your project to develop locally with docker, run the following command:
* Navigate to port 9000 on your host to see the documentation. This will be opened automatically at localhost for local, non-docker development.

```shell
docker compose -f local.yml up docs
```

*[Reference](https://cookiecutter-django.readthedocs.io/en/latest/document.html#)

# Additional Standard Practices

* Database should not be containerized and be in separate server
* For Containers:
    * For local deployment, best practice is to mount volume of app to accommodate dynamically changing source code. Do not convert to image.
    * Persistent storage (a.k.a media files) should not be in container. Common practice is to mount volume and link to media directory (follow the settings configuration. Find: "MEDIA_ROOT")

# Usage of Cookiecutter to create new project

Let's pretend you want to create a Django project called "redditclone". Rather than using `startproject`
and then editing the results to include your name, email, and various configuration issues that always get forgotten until the worst possible moment, get [cookiecutter](https://github.com/cookiecutter/cookiecutter) to do all the work.

First, get Cookiecutter. Trust me, it's awesome:

    $ pip install "cookiecutter>=1.7.0"

Now run it against this repo:

    $ cookiecutter https://github.com/codematsing/cookiecutter-django

Or, run using with configuration file

    $ cookiecutter https://github.com/codematsing/cookiecutter-django --config-file <path/to/cookiecutter.yaml> --no-input

*Sample of cookiecutter.yaml file*

```yaml
default_context:
    project_name: "project name"
    description: "project description"
    author_name: "Sam Solis"
    email: "sam.solis@codematsing.com"
    domain_name: "*.com"
    open_source_license: "None"
    use_elasticsearch: "y"
    windows: "y"
    use_pycharm: "n"
    use_docker: "y"
    postgresql_version: 1 #latest selection
    cloud_provider: "None"
    mail_service: "Other SMTP"
    use_async: "y"
    use_drf: "y"
    frontend_pipeline: "Django Compressor"
    use_celery: "y"
    use_mailhog: "n"
    use_sentry: "y"
    use_whitenoise: "y"
    use_heroku: "n"
    ci_tool: "Github"
    keep_local_envs_in_vcs: "y"
    debug: "n"
```

You'll be prompted for some values. Provide them, then a Django project will be created for you.

**Warning**: After this point, change 'Daniel Greenfeld', 'pydanny', etc to your own information.

Answer the prompts with your own desired [options](http://cookiecutter-django.readthedocs.io/en/latest/project-generation-options.html). For example:

    Cloning into 'cookiecutter-django'...
    remote: Counting objects: 550, done.
    remote: Compressing objects: 100% (310/310), done.
    remote: Total 550 (delta 283), reused 479 (delta 222)
    Receiving objects: 100% (550/550), 127.66 KiB | 58 KiB/s, done.
    Resolving deltas: 100% (283/283), done.
    project_name [My Awesome Project]: Reddit Clone
    project_slug [reddit_clone]: reddit
    description [Behold My Awesome Project!]: A reddit clone.
    author_name [Daniel Roy Greenfeld]: Daniel Greenfeld
    domain_name [example.com]: myreddit.com
    email [daniel-greenfeld@example.com]: pydanny@gmail.com
    version [0.1.0]: 0.0.1
    Select open_source_license:
    1 - MIT
    2 - BSD
    3 - GPLv3
    4 - Apache Software License 2.0
    5 - Not open source
    Choose from 1, 2, 3, 4, 5 [1]: 1
    timezone [UTC]: America/Los_Angeles
    windows [n]: n
    use_pycharm [n]: y
    use_docker [n]: n
    Select postgresql_version:
    1 - 14
    2 - 13
    3 - 12
    4 - 11
    5 - 10
    Choose from 1, 2, 3, 4, 5 [1]: 1
    Select cloud_provider:
    1 - AWS
    2 - GCP
    3 - None
    Choose from 1, 2, 3 [1]: 1
    Select mail_service:
    1 - Mailgun
    2 - Amazon SES
    3 - Mailjet
    4 - Mandrill
    5 - Postmark
    6 - Sendgrid
    7 - SendinBlue
    8 - SparkPost
    9 - Other SMTP
    Choose from 1, 2, 3, 4, 5, 6, 7, 8, 9 [1]: 1
    use_async [n]: n
    use_drf [n]: y
    Select frontend_pipeline:
    1 - None
    2 - Django Compressor
    3 - Gulp
    Choose from 1, 2, 3, 4 [1]: 1
    use_celery [n]: y
    use_mailhog [n]: n
    use_sentry [n]: y
    use_whitenoise [n]: n
    use_heroku [n]: y
    Select ci_tool:
    1 - None
    2 - Travis
    3 - Gitlab
    4 - Github
    Choose from 1, 2, 3, 4 [1]: 4
    keep_local_envs_in_vcs [y]: y
    debug [n]: n

Enter the project and take a look around:

    $ cd reddit/
    $ ls

Create a git repo and push it there:

    $ git init
    $ git add .
    $ git commit -m "first awesome commit"
    $ git remote add origin git@github.com:pydanny/redditclone.git
    $ git push -u origin master

Now take a look at your repo. Don't forget to carefully look at the generated README. Awesome, right?

For local development, see the following:

-   [Developing locally](http://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html)
-   [Developing locally using docker](http://cookiecutter-django.readthedocs.io/en/latest/developing-locally-docker.html)

# TODOs

* Change local.yml to mount app vs. converting to image

# Forked Cookiecutter Django

Powered by [Cookiecutter](https://github.com/cookiecutter/cookiecutter), Cookiecutter Django is a framework for jumpstarting
production-ready Django projects quickly.

-   Documentation: <https://cookiecutter-django.readthedocs.io/en/latest/>
-   See [Troubleshooting](https://cookiecutter-django.readthedocs.io/en/latest/troubleshooting.html) for common errors and obstacles