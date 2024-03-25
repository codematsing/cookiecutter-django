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
    * Functions: include typing
    * Datatypes:
        * Boolean: 
            * prepend with ``is_``
                * object identity (i.e. is_active)
                * present tense action (i.e. is_graduating)
            * prepend with ``has_``
                * possessive (i.e. has_children)
                * past_tense_action (i.e. has_graduated)
        * Integer:
            * if integer is a count, use ``num_`` instead of ``no_`` (this is because ``no`` can be used as prefix for boolean fields i.e. ``has_no_value``)

* Django
    * Directories
        * directories follow plural, snake case syntax
        * for multiple models complex models, might be best to create a directory of models.  or might be best to create nested applications
        * for nested applications, please ensure you adjust config.py to adjust location of app_name
        * Usual Application Files:
            * context_processors.py - passing variables to templates
            * templatetags.py - operational functions in templates
            * validators.py - validation for model and form fields
            * tables.py - djangotables2
            * filters.py - djangofilters
            * mixins.py - mixins are used to add functionality to views, forms, and models, allowing developers to reuse code and improve the efficiency of their applications 
            * signals.py
            * forms.py
            * serializers.py - DRF

    * Urls
        * route - dash as separators (due to SEO readability)
        * name - snakecase (python convention)

        .. code-block::

            # urls.py
            path(
                route='contact-us', 
                view=Contact.as_view(), 
                name="contact_us"
            )

    * Views.py

        .. code-block:: python

            from models import ModelA

            class ModelA<CRUD>View:...
            class ModelA<Action><Object>View:...
            # sample
            class ModelAUpdateStatusView:...

    * Ajax Views.py

        .. code-block:: python

            #ajax/views.py
            from models import ModelA

            class ModelAAjax<CRUD>View:...
            class ModelAAjax<Action><Object>View:...

    * Forms.py

        .. code-block:: python

            #ajax/views.py
            from models import ModelA
            
            # for generic form or model form
            class ModelAForm(ModelForm):...

            # for forms grouped together
            class ModelAFormCollection(FormCollection):...

            # for multiple instance of a singular form
            class ModelAFormset(FormCollection):...

    * Models.py
        * Model Class: singular, upper camel case
        * All Model Fields: include help_text, nullity convention, verbose name

            .. note::

                Providing these information will reduce the need to repeat 
                settings in forms if and when created. See also :ref:`overriding-sequence`

        * Foreign Field: include related name

            .. note::

                using ``cookiecutter-app`` also provides ``default_related_name`` for a model

        .. code-block:: python

            # Boolean fields: include choices
            is_bool = BooleanField(choices=[[None, "Pending"], [True, "Approve"], [False, "Reject"]])

            # Many to Many fields
            subjects = ManyToMany(Subject)

            # property methods
            def _private_method(self):
                pass

            # UI method helpers
            @property
            def as_html(self):
                # rendering object as html element. Similar functionality as __str__ but with html wrapping
                return render_to_string('detail_wrapper/<element>.html', object)

            @property
            def <field>_as_html(self):
                # render a local field as an html element
                # similar to get_status_display but with html wrapping
                return {field.name:getattr(self, field.name) for field in self._meta.fields}

            @property
            def as_card(self):
                # render object as a card
                # for a more custom card, place template in model template with title detail_card.html
                return render_to_string('detail_wrapper/table.html', self)

            # URL access helpers
            def get_<view>_url(self):
                pass

            # UI access helpers
            @property
            def c(self):
                # for indirect related models you can add bypass accessors
                # i.e. Model A || -- || Model B ||--|| Model C
                return self.b.c

            # Derived Fields
            @property
            def count_subjects(self):
                # consider as property method with intended name
                return self.subjects.count()

            @property
            def total_units(self):
                # consider as property method with intended name
                return self.subjects.num_units.sum()

            # Generic Functions
            def <action>_<return_value>_from_<params>(self, *params):
                return return_value

    .. note::

        Note: please also be guided with django coding conventions for generic coding guidelines 
        https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/



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

    models <- forms : "forms will modify models defaults"
    forms <- views : "views may change form customizations"
    models <-- views : "views may change default model form customizations"

By convention, global defaults should be placed in ``models.py``, as oppose to ``forms.py``.

Thus models are expected to be **explicit and precise** in order practice the *DRY principle*.
See :ref:`recommended mandatory model field options <overriding-sequence-models>` as a guide to excercising this rule.

.. important::

    It may be regarded as unnecessary that ``models.py`` is defined explicitly if eventually we expect to override fields in a form. 
    But it should be noted, that again, this serves as the root of any invocation in our project.

    Setting up as much information here would reduce the need to reset most information in forms and views,
    and even, eliminate the need to do modifications in ``forms.py`` and ``views.py``

    .. code-block:: python

        from models import Model
        from forms import ModelForm

        class ViewA:
            model = Model
            # let model have default boolean widget=checkbox

        class ViewB:
            model = Model
            form_class = ModelForm
            # let form modify widget=radioselect

        class ViewC:
            model = Model
            form_class = ModelForm

            def get_form_class(self, form):
                #widget=select
                return form

        # insights on this impl:
        # ViewA will rely on default customizations in models.py
            # ViewA will render widget=Checkbox
        # ViewB and ViewC will refer to modifications made by `ModelForm` on `Model`
            # ViewB and ViewC is initially set to render widget=checkbox
            # but due to modifications in ModelForm, widget=RadioSelect
        # View C will have additional modifications to its form that only View C will be affected
            # ViewC is the only view that will show widget=Select

.. note::

    After models, ``forms.py`` becomes the basis for setting up form fields. 
    As a practice, deviations from field settings in ``models.py`` are placed here.  
    Usually, reasons for creating a ``forms.py`` on top of presets in ``models.py`` are for the following functions:

    * Overriding default field widget. (i.e. Selectize, Date, File Widgets)
    * Overriding saving functionalities
    * Custom Formsets / Form Collections (see https://github.com/jrief/django-formset)
    * Reusability of forms to multiple views

    Finally, ``views.py`` provides the final catch for any customizations for forms for a particular view.
    Usually, customizations relating to forms are modified only in the following methods:

.. important::

    If your only sole purpose to create a form is to limit the number of fields that will be modified,
    Use fields / exclude instead in ``views.py``

    .. code-block::

        # scenario: we want a view that will only allow updating of
        # status and comment

        # models.py
        class Model:
            status = ...
            comment = ...
            detail1 = ...
            detail2 = ...

        # DONT USE forms.py
        # INSTEAD:

        # views.py
        class View:
            model = Model
            fields = ['status', 'comment']
            # or
            exclude = ['detail1', 'detail2']

Views Field Setups
++++++++++++++++++

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

Model Declarations
++++++++++++++++++

As a guide, it would be best to provide the following information of **ANY** field:

* null
* blank
* verbose_name
    * will also be the default form field label
* default
    * default value. Best to include especially when databases are growing, migrations will be easier to handle
* help_text
    * support field that will also be shown in forms
* validators
    * restrict values that will be captured
* choices
    * restrict values that will be captured if applicable
* unique
    * restricts values that will be captured

.. important::
    For `OneToOneField` and `ForeignKey`, it is adviseable to also add related name for is of access for related models

    .. code-block:: python

        # for OneToOneFields
        class Parent(models.Model):
            pass

        class Child(models.Model):
            # for one to one
            parent = OneToOneField(relate_name="child") # user verbose_name of child class
            # for foreign key or many to one
            parent = ForeignKey(relate_name="children") #use verbose_name_plural of child class
            class Meta:
                verbose_name="child"
                verbose_name_plural="children"

    Why do we want to want to be intentional in the setup of related_names?

    .. code-block:: python

        # for ease of access and quick understanding of relationship
        parent = Parent.objects.first()
        print(parent.children) 
        #we know that Parent model has a relationship with Childe model
        #we know that Parend instance can have multiple children

        print(parent.child)
        #we know that Parent model has a relationship with Childe model
        #we know that Parent instance has a one to one relationship with Child model

Furthermore, it would be best to provide the following information to the **Meta** class of a model:

* ordering
    * presets ordering of lists
    * best analogy is sorting of posts based on latest to oldest records
* get_latest_by
    * similar to ordering but specifically for `<model>.objects.last()`
* unique_together
* app_label
    * grouping of models
    * is seen when looking at admin page
* verbose_name
    * is often accessed to refer to model instance
* verbose_name_plural
    * is often accessed to refer to model list
* permissions

.. note::

    Though not mandated, it is optionally recommended to include ``db_table_comment`` in a model's **Meta** class.
    It will provide developers a brief explanation of the purpose of the table without viewing the 
    project documentation

Finally, as mentioned earlier, while widgets are normally set in forms, if we have multiple forms and formsets throughout our project
that will require consistent use of custom widget, we can instead create our custom field as referenced in: 
`Django Documentation <https://docs.djangoproject.com/en/4.2/howto/custom-model-fields/#specifying-the-form-field-for-a-model-field:~:text=the%20correct%20value.-,Specifying%20the%20form%20field%20for%20a%20model%20field,-%C2%B6>`_

.. note:: 

    Please refer to `utils.base_model.fields` for already preset custom model fields that use better widgets than
    that in vanilla django

    .. code-block:: python

        # since we are using jrief/django-formset library to handle file and image fields
        # rather than needing to create custom forms each time, instead use the impl below:
        from utils.base_models import fields, models
        class Document(models.AbstactBaseModel):
            attachment = fields.FileField(verbose_name=..., help_text=...)

    .. danger::

        **This implementation is still buggy**. Incorporating this to your system may
        cause issues with django admin pages.

        This is because templates for django admin pages do not support new widgets

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
    export $(grep -v '^#' $(pwd)/.envs/.local/.django | xargs)
    export $(grep -v '^#' $(pwd)/.envs/.local/.postgres | xargs)
    export $(grep -v '^#' $(pwd)/.envs/.local/.tokens | xargs)
    DATABASE_URL=postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_DB

* a predeactivate file is placed inside virtualenv to ensure env variables are unset when virtualenv is not used

.. code-block:: shell

    # /path/to/virtualenv/bin/predeactivate
    unset $(grep -v '^#' $(pwd)/.envs/.local/.django | sed -E 's/(.*)=.*/\1/' | xargs)
    unset $(grep -v '^#' $(pwd)/.envs/.local/.postgres | sed -E 's/(.*)=.*/\1/' | xargs)
    unset $(grep -v '^#' $(pwd)/.envs/.local/.tokens | sed -E 's/(.*)=.*/\1/' | xargs)


.. tip::

    .. code-block:: shell

        cp -r .envs/.local .envs/.<virtualenv_name>
        # setup custom flags for new environment
        vim .envs/.<virtualenv_name>/.<file>
        # replace paths to .envs/.local .envs/.<virtualenv_name>
        vim .envs/.<virtualenv_name>/activate
        vim .envs/.<virtualenv_name>/predeactivate
        virtualenv .<virtualenv_name>
        cp .envs/<virtualenv_name>/* .<virtualenv_name>/bin/activate

        # validation
        .<virtualenv_name>/bin/activate
        echo $POSTGRES_DB # or other env variables that have been changed