 .. _devtools:

Dev Tools
======================================================================

Tips and Tricks setup for developers during development of project

.. important::

    All scripts are expected to be run in root directory of the project

Documentation
-------------

Documentation of project shall be provided in docs. To run the documentation,
you may run the code below and access the documentation at http://localhost:9000

.. code-block:: shell

    # in root directory
    # for auto-refresh
    sphinx-autobuild docs docs/_build/html --port 9000
    # or for static doccumentation
    make -C docs/. livehtml

.. caution::

    A prerequisite to the documentation is plantuml.
    To ensure documentation is running properly, plantuml.jar is required in docs directory.
    See ``./docs/conf.py`` for plantuml call


Notebooks
-------------

Writing code blocks can be tedious and some exploratory work is needed to perfect writing functions and classes.

Django has a vanilla feature to test code in console: ``./manage.py shell``

However, we can further extend this feature with the use of Jupyter that can save notebooks and provide intellisense. 
You can run a notebook with the command below, and it will run similar to django's interactive shell

.. code-block:: shell

    # notebook
    ./manage.py shell_plus --notebook

    # lab
    ./manage.py shell_plus --lab

.. caution::

    Django initializer is needed to be imported to successfully import configuration
    for app. Ensure that you run this first in your notebook:

    .. code-block:: python
        
        import django_initializer
    
.. note::

    Automatically, Jupyter tree will load and show ``./notebooks`` directory.
    This is programmed so that notebooks are properly stored and organized, 
    and is ensured that they will not clutter root directory.
    Further settings can be seen at ``./config/settings/local.py``

DB Reset
-------------

During initial development, resetting db can be common task due to conflicts
caused by changes in models.py commit. Resetting db is not a direct task and
requires a certain approach:

* Clearing migration folders
* Deleteing database
* Recreating database

To simplify this sequence:

.. code-block:: shell

    # reset_migrations: resets all app migration directories
    ./manage.py reset_migrations

    # reset_db: recreates database
    ./manage.py reset_db

.. tip::

    If an error occurs with recreation of database due to active connections, try:

    .. code-block::

        # for linux
        sudo service restart postgresql
        # for mac
        sudo brew services restart postgresql

        # reset_db
        ./manage.py reset_db

.. danger::

    **NEVER** run in production server. 
    This will remove your database without any backup.

    Developers **MUST** remove reset_db.sh in production server

 .. _setup_environment_variables:

Setup Environment Variables
-------------

Environment variables can vary in diffent machines.
In our development, we prefer to have multiple environment files for different functions as the files can 
become overbearing and difficult to maintain if all configurations are set in one file.

By default and as a sample, our environment directory for local development is set inside ```.envs/.local```.
Any developer is allowed to set their distinct setup environment variables in this directory
provided that they don't include this in feature commits.

We can check the directory and see multiple files already placed:

* Django flags / configuration
* Postgres credentials
* Third-party tokens / credentials

For our app to read our environment files, we have provided a code snippet
located in ```config/settings/base.py```.

It can be seen from the code snippet that our environment variables are found
when an ```ENV_FILE_DIR``` variable is set. But by default we are setting it to
.envs/.local. It can also be seen that ENV_FILE_DIR can also accept a single file.

.. code-block:: python

    # Reading environment file
    ENV_FILE_DIR = os.environ.get("ENV_FILE_DIR", ".envs/.local")
    if ENV_FILE_DIR:
        if os.path.isdir(ENV_FILE_DIR):
            for env_file in list(filter(lambda env_file: env_file.startswith("."), os.listdir(ENV_FILE_DIR))):
                env.read_env(f"{ENV_FILE_DIR}/{env_file}")
        elif os.path.exists(ENV_FILE_DIR):
            env.read_env(ENV_FILE_DIR)

Hijack
-------------------------------

An added library to immediately change user that is logged in

.. note::

    Only users with is_superuser=True can use the hijack functionality
    and is only accessible during DEBUG=True setting