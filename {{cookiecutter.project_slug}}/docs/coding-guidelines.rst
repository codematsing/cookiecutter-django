.. _coding_guidelines:

Coding Guidelines
=======================

The most significant advantage of coding standards is that they increase the readability of source code. 
This is beneficial for two main reasons: they make it easier to understand and to read for others. 

Having a consistent coding style makes onboarding new developers much more accessible. 
They can quickly understand the codebase, and they can contribute in the same way. 

Additionally, this will increase efficiency and productivity within the team. 

Coding standards will ensure that everyone follows the same code if you’re coding software with a group.

Naming Conventions
-----------------------

* RST
    * Files: dash as separators

* Python
    * Files: snake case
    * Classes: upper camel case
        * Private methods: prefixed with ``_`` (i.e. ``_get_item``)
    * Functions: include typing
    * Datatypes:
        * Boolean: 
            * prepend with ``is_``
                * object identity (i.e. is_active)
                * present tense action (i.e. is_graduating)
            * prepend with ``has_``
                * possessive (i.e. has_children)
                * past_tense_action (i.e. has_graduated)

* Python Applications
    * Directory: plural, snake case
    * Model Class: singular, upper camel case
        * \* Field: include help_text, nullity convention, verbose name

            .. note::

                Providing these information will reduce the need to repeat 
                settings in forms if and when created. See also :ref:`overriding-sequence`

        * Foreign Field: include related name

            .. hint::

                Related names are what the model is called as foreign key

        * Boolean Field: include choices
        * Audit terms: if needed to include auditlog (See :ref:`third-party-libraries`)
            * history - auditlog foreign key
            * <created/updated/uploaded/etc>_at - timestamp
            * <created/updated/uploaded/etc>_by - user
    * Urls
        * route - dash as separators (due to SEO readability)
        * name - snakecase (python convention)

    .. code-block::

        # example
        path(
            route='contact-us', 
            view=Contact.as_view(), 
            name="contact_us"
        )
    * Classes
        * Views.py
            * <Model><CRUD>View
        * Ajax Views.py
            * <Model>Ajax<Action>View
        * Forms.py
            * Form - form or model form
            * FormCollection - multiple forms grouped together
            * Formset - multiple instance of a singular form
    * Model methods
        * Generic model method classifications:
            * urls - `get_<view>_url()`
            * breadcrumbs = `get_<view>_breadcrumbs(as_html)`
            * ui accessors = `as_<type>`, `field_as_<type>`
            * derived fields
            * related model accessors
            * functions = `<action>_<return_value>_from_<params>(*params)`
        * Add methods as needed for ease of and consistent element rendering
        * Instance object transformation or type casting - use `as_<type>` i.e. (as_df, as_html)

        # TODO add this in base_model

        .. code-block:: python

            # UI method helpers
            @property
            def as_html(self):
                # rendering object as html element. Similar functionality as __str__ but with html wrapping
                return render_to_string('detail_wrapper/<element>.html', object)

            @property
            def fields_dict(self):
                # render fields as dictionary
                return {field.name:getattr(self, field.name) for field in self._meta.fields}

            @property
            def <field>_as_html(self):
                # render a local field as an html element
                # similar to get_status_display but with html wrapping
                return {field.name:getattr(self, field.name) for field in self._meta.fields}

            def as_card(self, fields='__all__'):
                # render object as a card
                # for a more custom card, place template in model template with title detail_card.html
                return render_to_string('detail_wrapper/table.html', self)

            # UI access helpers
            @property
            def <related related_model>(self):
                # for indirect related models you can add bypass accessors
                # i.e. Model A || -- || Model B ||--|| Model C
                return self.b.c

            # Derived Functions
            @property
            def total_income(self):
                # consider as property method with intended name
                return self.income.sum()

            # Generic Functions
            def <action>_<return_value>_from_<params>(self, *params):
                return return_value

            def calculate_annual_salary_from_family_members(self):
                return sum(self.family_members.values_list('salary', flat=True))

    Note: please also be guided with django coding conventions for generic coding guidelines 
    https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/

        * for multiple models complex models, might be best to create a directory of models.
        or might be best to create nested applications
        * Nested applications - ensure you change config.py to adjust location of app_name
        * Additional Files:
            * context_processors.py - passing variables to templates
            * templatetags.py - operational functions in templates
            * validators.py - validation for model and form fields
            * tables.py - djangotables2
            * filters.py - djangofilters
            * mixins.py - mixins are used to add functionality to views, forms, and models, allowing developers to reuse code and improve the efficiency of their applications 
            * signals.py
            * forms.py
            * serializers.py - DRF



.. _overriding-sequence:

Overriding Sequence
-----------------------

Overriding and inheritance is one of the core concepts for Object-Oriented Programming.
Django projects follow the following overriding sequence. 

Understanding this sequence will help developers know when to override 
and **WHERE** it is appropriate to place overriding mechanisms.

.. uml::

    skinparam monochrome true
    skinparam shadowing false
    skinparam arrowThickness 0.7
    skinparam packageTitleAlignment left
    skinparam usecaseBorderThickness 0.4
    skinparam rectangleBorderThickness 1

    rectangle Models as models
    rectangle Forms as forms
    rectangle Views as views

    models <-- forms : ""
    forms <-- views : ""

By convention, global defaults of forms should be placed in ``models.py``, as oppose to ``forms.py``.

Thus models are expected to be **explicit and precise** in order practice the *DRY principle*.
See :ref:`recommended mandatory model field options <overriding-sequence-models>` as a guide to excercising this rule.

.. important::

    It may be regarded as unnecessary that ``models.py`` is defined explicitly if eventually we expect to override fields in a form. 
    But it should be noted, that again, this serves as the root of any invocation in our project.

    Setting up as much information here would reduce the need to reset most information in forms and views,
    and even, eliminate the need to preset create ``forms.py``.

    To cite example, for cases where you have a two views such as:

    * View A: does not use a predefined form
    * View B: uses a predefined form

    If you plan on placing default form settings in forms.py instead of in models.py,
    then View A will not reflect these settings

After models, ``forms.py`` becomes the basis for setting up form fields. 
As a practice, deviations from field settings in ``models.py`` are placed here.  
Usually, reasons for creating a ``forms.py`` on top of presets in ``models.py`` are for the following functions:

* Overriding default field widget. (i.e. Selectize, Date, File Widgets)
* Overriding saving functionalities
* Custom Formsets / Form Collections (see https://github.com/jrief/django-formset)
* Reusability of forms to multiple views

Finally, ``views.py`` provides the final catch for any customizations for forms for a particular view.
Usually, customizations relating to forms are modified only in the following methods:

* fields
    * when a form is not necessary, and particular fields are only needed to be shown in fields. 
    The simplest approach is to enumerate only the necessary fields
* exclude
    * if enumerating fields would be too tedious such that ``len(fields) >> len(exclude)``,
    it is adviseable to just provide excluded fields instead
* form
    * defined if a preset form is used to override `models.py` settings
* get_initial
    * presetting initial values
    
    .. code-block:: python

        def get_initial(self):
            initial = super().get_initial()
            initial.updated_by = self.request.user
            return initial

* get_form
    * should be used rarely, normally set to filter field choices dependent by current request parameters

    .. code-block:: python

        def get_form(self):
            form = super().get_form()
            form['field'].queryset = foo_model.objects.filter(bar_model=self.get_object())
            return form
    
.. _overriding-sequence-models:

Models
++++++

As a guide, it would be best to provide the following information of **ANY** field:

* null
* blank
* default
* verbose_name
* help_text
* validators
* choices
* unique

Furthermore, it would be best to provide the following information to the **Meta** class of a model:

* ordering
* get_latest_by
* unique_together
* app_label
* verbose_name
* verbose_name_plural
* permissions

.. tip::

    Though not mandated, it is optionally recommended to include ``db_table_comment`` in a model's **Meta** class.
    It will provide developers a brief explanation of the purpose of the table without viewing the 
    project documentation

Finally, as mentioned earlier, while widgets are normally set in forms, if we have multiple fields throughout our project
that will require consistent replacement of widget, we can instead create our custom field as referenced in: 
`Django Documentation <https://docs.djangoproject.com/en/4.2/howto/custom-model-fields/#specifying-the-form-field-for-a-model-field:~:text=the%20correct%20value.-,Specifying%20the%20form%20field%20for%20a%20model%20field,-%C2%B6>`_

.. _adding_custom_virtualenv:

Adding custom virtualenv
------------------------

Virtual environments (virtualenvs) serve a crucial purpose in software development.
They provide an isolated and self-contained environment for your projects, 
allowing you to manage dependencies, versions, and configurations independently for each project. 

The following steps must be followed when creating virtual envs:


* Create a virtualenv, run the following command

.. code-block:: shell

    virtualenv .<virtualenv>

* Add environment files for env variables

.. code-block:: shell

    .envs
    ├── .<virtualenv_name>
    │   ├── .django #custom django settings presets
    │   ├── .postgres # postgres credentials
    └── └── .tokens # additional credentials and other API tokens

* Replace/modify activate ``.<virtualenv>/bin/activate`` with the following modifications
  to ensure that postactivate and predeactivation scripts of environment variables will run

.. code-block:: shell

    # /path/to/virtualenv/bin/activate

    # find
    deactivate ()

    # paste inside
    if ! [ -z "${VIRTUAL_ENV}" ] ; then
        source ${VIRTUAL_ENV}/bin/predeactivate
    fi

    # find
    export PATH

    # paste
    source ${VIRTUAL_ENV}/bin/postactivate


* a postactivate file must be placed inside virtualenv to ensure env variables are exported


.. code-block:: shell

    # /path/to/virtualenv/bin/postactivate
    sudo service postgresql restart
    ROOT_DIR=$(dirname "$(dirname "$(dirname "$(realpath "$0")")")")
    export $(grep -v '^#' $ROOT_DIR/.envs/.vars/.commons | xargs)
    export $(grep -v '^#' $ROOT_DIR/.envs/.local/.django | xargs)
    export $(grep -v '^#' $ROOT_DIR/.envs/.local/.postgres | xargs)
    export $(grep -v '^#' $ROOT_DIR/.envs/.local/.tokens | xargs)

* a predeactivate file is placed inside virtualenv to ensure env variables are unset when virtualenv is not used

.. code-block:: shell

    # /path/to/virtualenv/bin/postactivate
    ROOT_DIR=$(dirname "$(dirname "$(dirname "$(realpath "$0")")")")
    unset $(grep -v '^#' $ROOT_DIR/.envs/.local/.django | sed -E 's/(.*)=.*/\1/' | xargs)
    unset $(grep -v '^#' $ROOT_DIR/.envs/.local/.postgres | sed -E 's/(.*)=.*/\1/' | xargs)
    unset $(grep -v '^#' $ROOT_DIR/.envs/.local/.tokens | sed -E 's/(.*)=.*/\1/' | xargs)

.. tip:: 

    Best to copy existing copy of environment in .envs (i.e. .local) and change values
    including postactivate and predeactivate scripts to new directory

.. tip:: 

    Run console command ``echo $POSTGRES_DB`` or other env variables 
    to see if activation/deactivation was successful


