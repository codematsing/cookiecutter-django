.. _third-party-libraries:
Third Party Libraries
======================================================================

Some of the adopted third-party-libraries used in this project are:
*  `django-allauth <https://django-allauth.readthedocs.io/en/latest/>`
    * Already adopted by django-cookiecutter

*  `django-formsets <https://django-formset.fly.dev/>`
    * A new approach to integrating formsets in project. 
    Please see formset documentation as their are built in items in the system
    that abstracts adoption of the library further and some rules to follow when
    using in system

*  `django-ajax-datatable <https://github.com/morlandi/django-ajax-datatable>`
    * An integrated approach to loading table data with searching, sorting functionality
    Please see datatable documentation as their are built in items in the system
    that abstracts adoption of the library further and some rules to follow when
    using in system

*  `django-comments-xtd <https://django-comments-xtd.readthedocs.io/en/latest/>`

*  `django-guardian <https://django-guardian.readthedocs.io/en/stable/>`
    * When per-object-permission is needed application to the system

*  `django-mptt <https://django-mptt.readthedocs.io/en/latest/>`
    * When tree-type model is needed in database design

*  `django-colorfield <https://github.com/fabiocaccamo/django-colorfield>`
    * When color inputs are needed. Particularly in setting up status badges