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

To simplify this instruction, a script is provided in the base folder

.. code-block:: shell

    # to reset db
    ./reset_db.sh

.. danger::

    **NEVER** run in production server. 
    This will remove your database without any backup.

    Developers **MUST** remove reset_db.sh in production server

Setup Initial Environment
-------------

During initial development, syncing environment based on the needs of the project can be a hassle.
Thus, we have created a script to initially setup environments. 
The benefit of such setup is that it also introduces files:
    * postactivate - loads environment variables based on mode of setup
    * predeactivate - unsets loaded environment variables

.. code-block:: shell

    $ python setup_venvs.py

Hijack
-------------------------------

An added library to immediately change user that is logged in

.. note::

    Only users with is_superuser=True can use the hijack functionality
    and is only accessible during DEBUG=True setting