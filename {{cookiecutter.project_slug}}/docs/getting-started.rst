.. _getting_started:

Getting Started
======================================================================

This section is focused on preparing for local development

.. warning::

    Getting started assumes that you have an **ubuntu linux OS**. 
    This is because servers are deployed in ubuntu servers.

    Replicating production server environments are best approach for development
    to avoid incompatibilities between local and production environment.

    .. tip::

        For windows users, suggest is to install windows subsystem for linux (WSL2)
        for development projects and follow instructions as follows

        For mac users, mac users can be natively support the development projects.
        Just research the brew installation counterpart for apt packages installations


* Base Requirements prior to starting a project
    * Through ubuntu apt package manager
        * `python <https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-an-ubuntu-20-04-server>`_
            * virtualenv
        * git
        * postgresql 
        * nginx (for production)
    * Through site
        * `pgadmin <https://www.pgadmin.org/download/>`_

* Starting project

    * If we are creating a repository from scratch (optional)

        .. code-block:: shell

            coookiecutter https://github.com/codematsing/cookiecutter-django

    * If repository exists, clone the project instead

        .. code-block:: shell

            git clone /path/to/repository

* Setup Database

    .. caution::

        Prerequisite for this is that postgresql is running

        .. code-block:: shell

            # to check nginx conf
            sudo service postgresql status
            # note the port number where postgresql is exposed

            # to start postgresql
            sudo service postgresql start

    * If you have a fresh install of postgresql with no user and password setup

        .. code-block:: shell

            # Refer to db and postgres user details to create
            cat .envs/.local_env/.postgres

            #tl;dr: 
            # Reference for interactive user creation: 
            # Create superuser for your rdbms
            # https://www.digitalocean.com/community/tutorials/how-to-use-roles-and-manage-grant-permissions-in-postgresql-on-a-vps-2
            sudo -i -u postgres
            createuser --interactive # quick creation with settings. create a superuser

            # Reference in setting up postgresql user: https://medium.com/coding-blocks/creating-user-database-and-adding-access-on-postgresql-8bfcd2f4a91e
            sudo -u postgres psql # running psql console as user postgres
            postgres=# CREATE DATABASE <dbname>;
            postgres=# ALTER USER <username> WITH encrypted password '<password>'; # creating non-root user
            postgres=# GRANT ALL PRIVILEGES on DATABASE <dbname> TO <username> ;

    * If you have an existing postgresql user and you don't want to create another user. Just update environment variables instead and create db

        .. code-block:: shell

            vim .envs/.local/.postgres # update database variables based on set credentials
            createdb <dbname> #based on POSTGRES_DB in file

    * **For production**: create a readaccess user

        .. code-block:: shell

            # for production environment
            # create a readaccess privileged user to restrict direct access to postgresql
            sudo -u postgres psql
            CREATE ROLE readaccess;

            -- Grant access to existing tables
            GRANT CONNECT ON DATABASE <dbname> TO readaccess;
            GRANT USAGE ON SCHEMA public TO readaccess;
            GRANT SELECT ON ALL TABLES IN SCHEMA public TO readaccess;

            -- Grant access to future tables
            ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO readaccess;

            -- Create a final user with password
            CREATE USER read_user WITH PASSWORD '<read_password>';
            GRANT readaccess TO read_user;

* Loading virtualenv and setting up app dependencies

    .. code-block:: shell

        # creation of virtualenv
        virtualenv .local_venv
        virtualenv .prod_venv #for production

        # activating virtualenv and installing app dependencies
        source .local_venv/bin/activate
        pip install -r requirements/local.txt

        # validate if.local_venv reflects set environment variables
        echo $POSTGRES_DB


    .. caution::

        If you are using mac os, you might need change ``.local_venv/bin/postactivate``
        for operations in restarting the database

* Populate database

    .. code-block:: shell

        ./manage.py makemigrations
        ./manage.py migrate
        ./manage.py load_dummy
        # override load_dummy to setup datatabse
        # initially, only creates superuser with credentials
        # username: admin
        # email: admin@example.com
        # password: qwer!@#$

* Testing project

    .. code-block:: shell

        ./manage.py runserver && xdg-open http://localhost:8000

* Starting sphinx documentation

    .. code-block:: shell

        # in root directory
        # for auto-refresh
        sphinx-autobuild docs docs/_build/html --port 9000
        # or for static doccumentation
        make -C docs/. livehtml

* Create application using Cookicutter-app (not django-admin startapp)

    Improvement to ``django-admin startapp``.
    Includes tests and factories in generation of app.

    .. code-block:: shell

        cd apps

        # must be inside apps
        coookiecutter ../utils/cookiecutter-app 

.. tip::

    Please be guided with :ref:`coding_guidelines` and :ref:`modifications` moving forward
