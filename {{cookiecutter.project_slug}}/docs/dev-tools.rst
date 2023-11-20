 .. _devtools:

Dev Tools
======================================================================

Tips and Tricks setup for developers during development of project

.. note::

    All scripts are expected to be run in root directory of the project

Documentation
-------------

Documentation of project shall be provided in docs. To run the documentation,
you may run the code below and access the documentation at http://localhost:9000

.. code-block:: shell

    make -C docs livehtml

.. note::

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

.. tip::

    If you are running jupyter notebook in vscode, setting notebook python interpreter to:
    ``/path/to/project/.local_env/bin/python`` will not require running a jupyter server


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