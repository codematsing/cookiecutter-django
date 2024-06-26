.. _testing:

Testing
========

Unit testing and UI testing are integral components of a comprehensive software testing strategy. 

Unit testing focuses on verifying the correctness of individual units or components in isolation, 
allowing developers to catch bugs early in the development process. 
By promoting code modularity and providing a safety net for refactoring, 
unit tests contribute to the maintainability and reliability of the codebase. 

They also serve as documentation, guiding developers on expected behaviors and facilitating collaboration. 
Additionally, unit tests play a crucial role in regression testing, 
preventing the inadvertent introduction of new bugs during code changes.

On the other hand, UI testing validates the end-to-end functionality of the user interface, 
ensuring a seamless user experience. It addresses critical aspects such as cross-browser compatibility, 
cross-device functionality, and the validation of key user flows. 

UI tests are essential for detecting issues that may arise from the integration of business logic 
and play a pivotal role in assuring the overall quality and usability of the application. 

Together, unit testing and UI testing provide a robust defense against software defects, 
promoting software reliability, maintainability, and a positive user experience.


Factories
----------

Before going over the different types of testing, we go over implementation of factories in Django.

Factories are key in doing testing as they generate mock data in early stages of development.

Using ``cookecutter-app`` already provides a placeholder for our Factories in ``<app_name>/tests/factories.py``.

.. tip:: 
    
    You can register factories in conftest.py to easily access factories in different tests.

.. hint::

    Refer to `FactoryBoy <https://factoryboy.readthedocs.io/en/stable/orms.html>`_ and `Faker <https://faker.readthedocs.io/en/master/>`_ for proper setup of model factories.

.. caution::

    Our system includes a mocking mechanism for media files. This is located in ``file_management/tests/factories.py``.

    This mechanism **generates actual pdf files** in ``base/media/`` directory.

    To avoid bloating your local development project folder, running ``./reset_db.sh`` includes removing of media files

Unit Testing
----------

There are already initial set of test files that are pregenerated when using ``cookiecutter-app``.

If developers plan to integrate unit testing to site, consider the matter of sequence of importance and implementation for the following files:

* test_models
    * check appropriate implementation of custom model methods
* test_signals
    * check affectation of saving one model to another model based on signal implementation
    * check routing notifications triggered by signals
* test_forms
    * check custom form validation and saving
    * if there is no custom model form but we would want to test different use cases for models, we can invoke ``get_errors`` from ``utils/validators``:

        .. code-block:: python

            # test_forms.py
            from app_name.models import Model
            from utils.validators import get_errors
            class ModelFormsTestCase(TestCase):
                def setUp(self):
                    self.object = ModelFactory()

                def test_model_full_clean(self):
                    instance = Model() 
                    # instantiate variables
                    instance.var1 =... 
                    instance.var2 =... 
                    self.assertTrue(get_errors(instance)=={})


* test_urls
    * simulate permissions and error codes to be received by logged user
* test_views
    * test appropriate templates used when invoking traversal to a specific url

Pytest
^^^^^^

This project uses the Pytest_, a framework for easily building simple and scalable tests.
After you have set up to `develop locally`_, run the following commands to make sure the testing environment is ready: ::

    $ pytest

You will get a readout of the `users` app that has already been set up with tests. If you do not want to run the `pytest` on the entire project, you can target a particular app by typing in its location: ::

   $ pytest <path-to-app-in-project/app>

If you set up your project to `develop locally with docker`_, run the following command: ::

   $ docker-compose -f local.yml run --rm django pytest

Targeting particular apps for testing in ``docker`` follows a similar pattern as previously shown above.

Coverage
^^^^^^^^

You should build your tests to provide the highest level of **code coverage**. You can run the ``pytest`` with code ``coverage`` by typing in the following command: ::

   $ docker-compose -f local.yml run --rm django coverage run -m pytest

Once the tests are complete, in order to see the code coverage, run the following command: ::

   $ docker-compose -f local.yml run --rm django coverage report

.. note::

   At the root of the project folder, you will find the `pytest.ini` file. You can use this to customize_ the ``pytest`` to your liking.

   There is also the `.coveragerc`. This is the configuration file for the ``coverage`` tool. You can find out more about `configuring`_ ``coverage``.

.. seealso::

   For unit tests, run: ::

      $ python manage.py test

   Since this is a fresh install, and there are no tests built using the Python `unittest`_ library yet, you should get feedback that says there were no tests carried out.

.. _Pytest: https://docs.pytest.org/en/latest/example/simple.html
.. _develop locally: ./developing-locally.html
.. _develop locally with docker: ./developing-locally-docker.html
.. _customize: https://docs.pytest.org/en/latest/customize.html
.. _unittest: https://docs.python.org/3/library/unittest.html#module-unittest
.. _configuring: https://coverage.readthedocs.io/en/v4.5.x/config.html

UI Testing
----------

Best approach to do unit testing is to first declare factories per model that have been created. 
After factories have been set, adjust script in ``base/mock_data/management/commands/load_dummy.py``.

This will populate the site with dummy data to properly test UI.