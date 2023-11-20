Project Structure
======================================================================

.. _project_structure_env_files:

* {{cookiecutter.project_name}} (base)
    * static - placement for static assets
    * media - location for uploaded media
    * templates - html and email templates
    * logs - logs
    * <commands> - location for django-admin commands
        * mock_data - ``./manage.py load_data`` script location. See `Factories <https://factoryboy.readthedocs.io/en/stable/>`_.
        * test_email - ``./manage.py test_email`` script location to test email credentials.
* config
    * settings - placement of settings files
* utils - see :ref:`util_modules`
* apps - see :ref:`app_modules`
* requirements - requirements.txt
* notebooks - placeholder for jupyter notebooks
* docs - placeholder for documentaton

Environment Files
-----------------

There are directories placed under ``.env``

* .vars - base copy of environment variables to be used
* .local - environment variables used during development and testing
* .production - environment variables used during production

.. note::

    Additional environment directories can be added when needed. (i.e. specific configuration for test server).
    However, structure is recommended to be followed for consistency.

    See :ref:`adding_custom_virtualenv` to see appropriate actions when setting up different
    configurations for different servers

.. tip::

    Variables can both be set in ``.vars`` and another env directory 
    as both directories will be loaded and sequentially.
    Thus, any variable set twice, will follow env directory value