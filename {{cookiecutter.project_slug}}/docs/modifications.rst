.. _modifications:

Modifications
======================================================================

Due to the expansion and specification of use cases of projects,
I have done some modifications that are more tailor fit to the usual use cases experienced.
Furthermore, some of these improvements are to prepare and automate some processes that are also normally tediously corrected or fixed

.. _cookiecutter_app:

Cookiecutter-app
-------------------------------

Cookiecutter-app is an improvement to the `django-admin startapp` script.
The Cookiecutter-app creates a django application that initializes the following files:

* apps.py
    * automatically imports `<app>/signals.py` which the vanilla does not which causes signals.py not to work from the get-go.
* admin.py
    * automatically registers application model for admin access
* urls.py
    * automatically preregisters a url for each CRUD view
* views.py
    * automatically presets a view for each CRUD view and mapped to our base template
* models.py
    * automatically presets a model inheriting audit log and base model mixin
* tests
    * adds placeholder for tests
* ajax
    * adds placeholder for ajax views and functionalities
* tests/factories.py
    * adds placeholder for dummy data factory

Setup
^^^^^

Cookiecutter-app will request for the following information 
and confirms inputs for the different formatting it will be used for 
in the app

* app_name: serves as the app directory name
    * app_name_snake_case_plural
    * app_name_verbose_name
* model_name: serves as the model name attributed to the app_name
    * model_name_camel_case
    * model_name_snake_case_plural
    * model_name_verbose_name_plural
    * model_name_snake_case
    * model_name_verbose_name
* app_location: mapping of where exactly the application is located from :file:`apps` directory as root
    * app_location_dot_notation
* view_prefix: identifies what time of template and view permission it will follow
* db_table_comment: brief description to the 

.. code-block::

    snake_case: an_example
    camel_case: AnExample
    verbose_name: An Example

Site Migration
-------------------------------

By default cookiecutter adds a sites mgiration folder in `base/contrib/migrations`
Some improvements were done to the migrations files so as to ease developers 
when switching between local, test and production servers.

Modifications preloads the following sites in site model:
1. localhost:8000
2. production server
3. test server

.. note:: 
    
    * Due to site switching, :file:`.env/.django` fles would declare a :code:`SITE_ID`
    * Due to site switching, :code:`utils.lambdas.get_current_domain` will adjust according to selected :code:`SITE_ID`
    * Advantage of this is that when we are testing emails have anchor tags referring to the site, clicking those anchor tags would redirect to the site that the email has been sent from

    .. code-block:: html

        <!-- Please refer to the following for email templates to ensure prepending of domain name in urls: -->
        {% load util_tags %}

        <a href="{{object.get_full_absolute_url}}">{{object}}</a>
        <a href="{% full_url 'app_name:view' arg1=arg1 arg2=arg2 %}">title</a>

User Authentication
-------------------------------

By default django-allauth integration of cookiecutter places a :file:`users/adapters.py`
which ensures integration for social authentication.

However, since we are managing organizational systems, sometimes it is a prerequisite to only accept
login using organization email.

.. hint::

    We setup :code:`RESTRICT_LOGIN_DOMAINS` and :code:`WHITELIST_LOGIN_DOMAINS` 
    in :file:`settings/base.py` and :file:`.envs/.django to toggle this condition`

    For example:
        * We want to accept google emails as valid login
            * :code:`RESTRICT_LOGIN_DOMAINS=False`
        * We want to only accept :code:`up.edu.ph` emails
            * :code:`RESTRICT_LOGIN_DOMAINS=True`
            * :code:`WHITELIST_LOGIN_DOMAINS=['up.edu.ph']`

    .. tip::
        
        see ``apps/users/adapters.py`` for logic implementation for ``ALLOWED_LOGIN_DOMAINS``

Base Models
-------------------------------

By default we are following vanilla django model fields.

The shortcoming however of declaring model fields based on vanilla django will also preset to default form widgets.
Default widgets can be outdated sometimes such as the default select widget that does not have intuitive search functionality.

To solve this issue, django uses :file:`forms.py` to customize form widgets which sometimes can be added burden if the only purpose of creating forms is to adjust form widgets.
The approach introduced in :file:`utils/models/fields.py` is to `preset the widget when model field is declared <https://stackoverflow.com/questions/28497119/change-default-widgets-of-django-to-custom-ones>`_ already

.. hint::
    
    Before we opt to user :code:`django.db.model` fields, check first or try to implement
    a new custom :code:`utils.base_models` field

History
^^^^^^^

In most cases, stakeholders require an audit trail due to the transactional nature of records.
To accommodate this need, a quick inheritance will quickly allow the system to track and render
a model instance's history

.. code-block:: python

    from utils.base_models.models import AbstractAuditModel
    class TrackedModel(AbstractAuditModel):
        ...

Base Forms
-------------------------------

The improvements made to base forms is the use of 
`Jacob Rief's django-formset extension <https://www.google.com/search?q=jrief%2Fdjango-formset&oq=jrief%2Fdjango-formset&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCDQ4MDlqMGoxqAIAsAIA&sourceid=chrome&ie=UTF-8>`_.

The purpose for using his library are due to adoption on the following issues:

* outdated vanilla django form widgets
* lack of conditional form fields handling
* static nature of django formset

The implementation of :file:`utils/base_forms/forms.py` is just to be the inherited parent class for 
our forms to adopt Jacob Rief's extension

.. code-block:: python

    #Adopt implement in model's forms.py
    from utils.base_forms.forms import BaseModelForm, BaseFormCollection
    class ModelForm(BaseModelForm):
        ...

    class ModelFormCollection(BaseFormCollection):
        ...


Base Views
-------------------------------

The improvements made to base views is the initialization of CRUD views
and to perform the initial permission checks as well as declare the appropriate
base template to use by the view

We adopted `plus admin templates <https://www.bootstrapdash.com/product/plus-admin>`_
in our framework because it has a coherent template design for:

* sidebar / admin pages (regarded as **admin pages** in our framework)
* top navbar / landing pages (regarded as **public pages** in our framework)

.. hint::

    When running `Cookiecutter-app`_, it will ask of the type of view you are asking, whether **admin** or **public**

Additionally, :code:`DetailView` also has an extra implementation to it where we preload a page based on 
:code:`object.as_card` property method

.. note::

    Some modification made base ``BaseView`` inherited are introduction of ``hidden_fields`` and ``disabled_fields``

Apps
----

Some apps are already pre-coded for us both by cookiecutter and additional apps
that are constantly needed by stakeholders

Users
^^^^^

Default implement by django-cookiecutter. 
Essentially removes the delineation of :code:`first_name` and :code:`last_name` and combines it to a new field :code:`full_name`. 

This is done having first and last names are cultural.
Thus, full_name provides a catch-all scenario.

Tags
^^^^

Statuses and tags are common in transactional models. To provide customization to statuses, 
such as color-coding, a model is provided as guide.

.. hint::

    Rather than copy-pasting the model, it might be best to inherit the :code:`BaseTag` instead

    .. code-block:: python

        from tags.models import BaseTag

        class Status(BaseTag):
            ...


File Management
^^^^^^^^^^^^^^^

File management app is already provided. 
The purpose for file management app is for centralization of files for ease of file tracking.

This uses the concept `GenericRelation <https://docs.djangoproject.com/en/5.0/ref/contrib/contenttypes/>`_ 
(analogous to ForeignKeys).

Furthermore, file management already provides property methods to embed files in a page.

.. important::

    Our system does not use default pdf renderers of whichever web browser a user interacts with.
    We adopt pdfjs for file rendering due to the nature of documents stored in our systems.

    Sometimes, stakeholders request that files are non-downloadable to comply with data privacy policies and regulations.

Posts
^^^^^

Most times systems require a blog posting mechanism for announcements that are viewable in landing pages.
This model provides the basic implementation for a blog post.

User Registration
^^^^^^^^^^^^^^^^^

Most times user login is restricted if not only by email authentication, but also by credentials.

Providing credential logins are also required to be restricted through moderation of user reqgistration requests.
This module provides that functionality.

.. uml::

    User -> System : Registers
    Moderator -> System : Checks user registrations
    Moderator -> System : Approves / Rejects registration
    System -> User : Notifies user
    alt User is approved
        User -> System: Creates User Credentials
    end
    
Module Management
^^^^^^^^^^^^^^^^^

Sets up sidebar items for client admin pages.

This module management introduces a middleware to check if a user has access by checking its group access.

.. uml::

    User -> System : Access client admin
    System -> System : Checks accessible modules (see module_management/ajax/views.py)
    System -> User : Returns UI with sidebar items
    User -> System : Access link
    System -> System : Checks link accessibility (see module_mangaement/ajax/middleware.py)
    alt link is accessible
        System -> User: Returns UI
    else link is NOT accessible
        System -> User: Forbidden
    end

.. tip::

    To setup client admin sidebar data, you may do the following:

    * go to django-admin and setup sidebar items there
    * go to `Modules` module in sidebar (if already set and existing)
    * setup load_dummy to include sidebar items

Group Management
^^^^^^^^^^^^^^^^^

Role / Group Management with incorporation of Module Management

Media Storage and File Encryption
---------------------------------
Due to the nature of serving media files by webservers, extra security is needed
to ensure that file classifications are followed when users force access media urls.

.. uml::

    User -> System : access media
    System -> System: Checks media accessibility
    alt User has access:
        System -> User: Returns media
    else User has NO access:
        System -> User: Returns 404
    end

Storages
^^^^^^^^

See utils/storage.py

Storage introduce a separate storage space for internal documents and public documents.

These storages shall be called by custom FileFields and ImageFields that dictate location of document.

The reason why storage only has public and internal file storage is because and internal file may easily
jump between internal, confidential or restristricted.

File Encryptor
^^^^^^^^^^^^^^

See utils/file_encryptor.py

File encryptors renames files for extra encryption. They contain information as to file access subclassification

.. tip::

    For ease of incorporation of FileEncryptor, use utils.lambdas.py functions to during
    development of model fields

    .. code-block:: python

        from utils.lambdas import public_upload, internal_upload, confidential_upload, restricted_upload
        from utils.base_models.fields import PublicImageField, InternalImageField, PublicFileField, InternalFileField

        class Model(models.Model):
            public_image = PublicImageField(upload_to=public_upload)
            public_attachment = PublicFileField(upload_to=public_upload)
            internal_attachment = InternalFileField(upload_to=internal_upload)
            confidential_attachment = InternalFileField(upload_to=confidential_upload)
            restricted_attachment = InternalFileField(upload_to=restricted_upload)
