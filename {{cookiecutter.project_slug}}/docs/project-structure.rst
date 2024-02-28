Project Structure
======================================================================

.. _project_structure_env_files:

* base
    * templates - html and email templates
    * static - placement for static assets
    * media - location for uploaded media
    * fixtures - dump for fixtures
    * logs - log files
    * contrib - dump for initial site migrations
    * <commands> - location for django-admin commands
        * mock_data - ``./manage.py load_data`` script location. See `Factories <https://factoryboy.readthedocs.io/en/stable/>`_.
        * test_email - ``./manage.py test_email`` script location to test email credentials.

    .. hint::

        Base folder is the "Python package for your project"

        Usually it is the placeholder for management and orchestration of the project.
        
        Due to django-cookiecutter template, some of the files are offloaded to config directory
* config
    * settings - placement of settings files
    * api.py, asgi.py, wsgi.py - placement of deployment files
    * urls.py - url declarations; a “table of contents” (root level) of site
* utils - see :ref:`util_modules`
* apps - see :ref:`app_modules`
* requirements - requirements.txt
* notebooks - placeholder for jupyter notebooks
* docs - placeholder for documentaton

Environment Files
-----------------

There are directories placed under ``.env``

* .tokens - credentials and tokens from external applications
* .local - environment variables used during development and testing
* .production - environment variables used during production

.. note::

    Additional environment directories can be added when needed. (i.e. specific configuration for test server).
    However, structure is recommended to be followed for consistency.

    See :ref:`adding_custom_virtualenv` to see appropriate actions when setting up different
    configurations for different servers

.. tip::

    If you have override custom declarations of settings or prefer to create another file
    set of environ variables, change reference in :file:`._env/bin/postactivate`
    to point to new environment files