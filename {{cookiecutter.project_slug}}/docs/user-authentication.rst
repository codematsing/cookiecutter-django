User Authentication
======================================================================

Custom Settings
----------------------------------------------------------------------
Logic flow as follows in 'account/login.html'


.. code-block:: html

    {% raw %}
    {% if get_settings_value ALLOW_SOCIAL_AUTH_LOGIN %}
        # show social auth providers login
        # by default google
    {% endif %}

    {% if get_settings_value ALLOW_NATIVE_LOGIN %}
        # show standard credential login

        {% if ACCOUNT_ALLOW_REGISTRATION %}
            {% if get_settings_value MODERATE_USER_REGISTRATION %}
                # redirect to registration form
            {% else %}
                # fallback to allauth user registration
            {% endif %}
        {% endif %}
    {% endif %}
    {% endraw %}