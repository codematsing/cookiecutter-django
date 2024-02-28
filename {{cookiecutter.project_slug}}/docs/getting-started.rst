.. _gettingstarted:

Getting Started
======================================================================

This section is focused on preparing for local development

* Base Requirements prior to starting a project
    * python
    * cookiecutter
    * virtualenv
    * git

* Starting a project with custom cookicutter

    .. code-block:: shell

        coookiecutter https://github.com/codematsing/cookiecutter-django

* If repository exists, clone the project instead

    .. code-block:: shell

        git clone /path/to/repository

* Loading virtualenv

    .. code-block:: shell

        python setup_venvs #helper script to create virtualenvs
        source .local_env/bin/activate
        pip install -r requirements/local.txt

    .. note::
    
        ``.local_env`` is a preloaded virtualenv that follows the rules in
        :ref:`adding_custom_virtualenv`

* Testing project

    .. code-block:: shell

        ./manage.py runserver && xdg-open http://localhost:8000

* Install postgresql and setup postgresql user
    
    .. code-block:: shell

        #tl;dr: 
        # Reference for interactive user creation: 
        # https://www.digitalocean.com/community/tutorials/how-to-use-roles-and-manage-grant-permissions-in-postgresql-on-a-vps-2
        sudo -i -u postgres
        createuser --interactive # quick creation with settings

        # Reference in setting up postgresql user: https://medium.com/coding-blocks/creating-user-database-and-adding-access-on-postgresql-8bfcd2f4a91e
        sudo -u postgres psql # running psql console as user postgres
        postgres=# CREATE USER <username> WITH encrypted password '<password>'; # creating non-root user

        # or
        postgres=# ALTER USER <username> WITH encrypted password '<password>'; # creating non-root user
        postgres=# GRANT ALL PRIVILEGES on DATABASE <dbname> TO <username> ;

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

* Setting up initial database

    .. code-block:: shell

        ./manage.py makemigrations
        ./manage.py migrate
        ./manage.py load_dummy
        # override load_dummy to setup datatabse
        # initially, only creates superuser with credentials
        # username: admin
        # email: admin@example.com
        # password: qwer!@#$

* Starting sphinx documentation

    .. code-block:: shell

        # in root directory
        # for auto-refresh
        sphinx-autobuild docs docs/_build/html --port 9000
        # or for static doccumentation
        make -C docs/. livehtml

* Starting applications using Cookicutter-app

    Improvement to ``django-admin startapp``.
    Includes tests and factories in generation of app.

    .. code-block:: shell

        cd apps

        # must be inside apps
        coookiecutter ../utils/cookiecutter-app 

.. tip::

    Please be guided with :ref:`coding_guidelines` moving forward
