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

        python setup_venvs.py
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
        # Reference for interactive user creation: https://www.digitalocean.com/community/tutorials/how-to-use-roles-and-manage-grant-permissions-in-postgresql-on-a-vps-2
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
        ./manage.py createsuperuser

        # username: admin
        # email: admin@example.com
        # password: qwer!@#$

* Starting applications using Cookicutter-app

    Improvement to ``django-admin startapp``.
    Includes tests and factories in generation of app.

    .. code-block:: shell

        cd apps

        # must be inside apps
        coookiecutter cookiecutter-app 

.. tip::

    Please be guided with :ref:`coding_guidelines` moving forward

Third-party Libraries
---------------------

Some of the libraries that are adopted in base project are:

* `django-formset <https://github.com/jrief/django-formset>`_
    * This library handles single forms and collections of forms with a way better user experience than the internal Django implementation for formsets offers.
* `django-ajax-datatable <https://github.com/morlandi/django-ajax-datatable>`_
    * Provides advanced integration with the jQuery Javascript library DataTables.net
    * Extended with custom code see :ref:`base_views`
* `django-colorfield <https://pypi.org/project/django-colorfield/>`_
    * Simple color field for your models with a nice color-picker in the admin-interface.
* `django-guardian <https://github.com/django-guardian/django-guardian/tree/55beb9893310b243cbd6f578f9665c3e7c76bf96>`_
    * Per object permission handling
* `django-tables2 <https://django-tables2.readthedocs.io/en/latest/>`_
    * Rendering of list tables. 
    * For catch cases that django-ajax-datatable cannot do
        * checkbox columns
        * data rendering from dataset, not models
* `django-filters <https://django-filter.readthedocs.io/en/stable/>`_
    * Django-filter is a generic, reusable application to alleviate writing some of the more mundane bits of view code. 
      Specifically, it allows users to filter down a queryset based on a model’s fields, displaying the form to let them do this.
* `django-mptt <https://django-mptt.readthedocs.io/en/latest/>`_
    * It takes care of the details of managing a database table as a tree structure and provides tools for working with trees of model instances.
* `reportlab <https://www.reportlab.com/>`_
    * PDF Generation
* `django-xtd-comments <https://django-comments-xtd.readthedocs.io/en/latest/>`_
    * A Django pluggable application that adds comments to your project.
* `django-auditlog <https://github.com/jazzband/django-auditlog>`_
    * django-auditlog (Auditlog) is a reusable app for Django that makes logging object changes a breeze. 
      Auditlog tries to use as much as Python and Django's built in functionality to keep the list of dependencies as short as possible. 
      Also, Auditlog aims to be fast and simple to use.
* `django-notifications-hq <https://github.com/django-notifications/django-notifications>`_
    * django-notifications is a GitHub notification alike app for Django, 
      it was derived from django-activity-stream
* `djangorestframework <https://www.django-rest-framework.org/>`_
    * Django REST framework is a powerful and flexible toolkit for building Web APIs.