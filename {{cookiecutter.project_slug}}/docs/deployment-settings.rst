===================
Deployment Settings
===================

Setting up environment variables in a deployment is an essential part of configuring and securing your application. 
Environment variables allow you to store sensitive information, configuration settings, and API keys outside of your codebase. 
Here's how to set up environment variables for deployment:

1. Creating .env file
2. Defining environment variables
3. Add .env in .gitignore
4. Loading environment variables in project

.. important::

    Guideline for loading variables should **NOT** be from accessing and reading environment files, 
    but rather through reading the server's running environment. This is to ensure security and maintaining
    anonimity of source file of env variables.

Systems are currently in place to ensure that environment variables are directly read through ``os.environ``

.. hint:: 

    See :ref:`adding_custom_virtualenv` to see how environment variables are loaded to the system

Loading environment data in project
-----------------------------------

Following rules are set in reading environment variables to the project:

* Reading via os.environ:
  * This ensures that we are reading env variables exported in os system
* Boolean variables are read and should be evaluated as string
* A default value must be provided inside project settings if not read in environment

Sample that reflects all these rules are shown below

.. code-block:: python

    # in settings.py
    DEBUG = os.environ.get("DEBUG", "False") == "True"

.. note::

    If additional vairables are needed to be added, just place them in .env files.
    See :ref:`Project Structure <project_structure_env_files>` for placement guide.