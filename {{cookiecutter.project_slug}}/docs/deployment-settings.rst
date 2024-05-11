===================
Deployment Settings
===================

.. uml::

    partition "Set up Server" {
        :add pub keys of developers;
        :clone repositories;
        :setup project dependencies;
    }
    partition "Third-party libraries" {
        split
            :Google Oauth Authentication;
        split again
            :Google SMTP;
        split again
            :Sentry Application Monitoring;
        split again
            :Github Workflow Actions;
        split end
    }
    partition "Set up Application for Production" {
        :configure environment variables;
        :handle static files;
        :bind gunicorn wsgi configuration;
    }
    partition "Setup network routing" {
        :nginx/apache app routing;
        :ssl certification;
    }

Setup Server
------------

    * `Pubkey setup <https://www.digitalocean.com/community/tutorials/how-to-configure-ssh-key-based-authentication-on-a-linux-server>`_
    * `Clone Repository via SSH<https://www.google.com/amp/s/dylancastillo.co/how-to-use-github-deploy-keys/amp/>`_
    * Refer to :ref:`Getting started <getting_started>`

    .. warning::

        Make sure for production level that you place your repository inside /var/www/html.

        Besides following deployment standard practices. This will reduce the headaches for permission related concerns.

Third-party Libraries
---------------------

Google Oauth
++++++++++++

    * Go to `Google Developer API Console <https://console.cloud.google.com/apis/dashboard>`_ and create / select a project

        .. image:: media/select_a_project.png

    * Create an Oauth Consent

        .. image:: media/oauth_consent.png

    * Go to credentials Tab and Create and OAuth Client ID

        * Application Type: Web Application
        * Name : Project Domain 
        * Authorized Javascript Origins: 
            [http://<domain name>, https://<domain name>, http://localhost:8000, http://127.0.0.1:8000]
        * Authorized Redirect URIs: 
            [http://<domain name>, https://<domain name>, http://localhost:8000, http://127.0.0.1:8000]/accounts/google/login/callback/

        .. image:: media/authorized_javascript_origins.png

        .. image:: media/authorized_redirect_uris.png

    * Add generated cliend ID and secret to ```.envs/*/.tokens```
    
        .. code-block:: shell

            GOOGLE_CLIENT_ID=<client_id>
            GOOGLE_SECRET_KEY=<client_secret>

    * Create sites for each domain where Oauth will be used
        * Create sites (by default ```base/contrib/sites/migrations``` will create sites during migrations)
            * You may add more sites using django admin or shell

        * Select sites that will use Oauth
        .. image:: media/socialauth.png

Setup SMTP
++++++++++++

    * Go to Gmail settings Forwarding and POP/IMAP tab
    
        .. image:: media/SMTP_settings.png

    * Go to `Gmail Account Security Settings <https://myaccount.google.com/security>`_
    * Go to 2-Step Verification > App passwords (bottom option)
    * Create app name: `SMTP`

        .. image:: media/SMTP_create_password.png

        .. image:: media/SMTP_password.png

        .. important::

            Make sure to copy the app password

    * Encode SMTP details in ```.env/*/.tokens```

        .. note::
            
            EMAIL_HOST_PASSWORD is based on generated 16-character password
            from previous step

        .. image:: media/SMTP_credentials.png

Sentry
++++++

`Create a sentry token <https://docs.sentry.io/api/guides/create-auth-token/>`_ and encode in ```.envs/*/.tokens``` with ```SENTRY_DSN``` variable

Github Workflow Action
++++++++++++++++++++++

.. caution:: 

    #TODO: This section is still under construction

Set up Application for Production
---------------------------------

.. tip::

    If you will follow link references, make sure to eventually replace the 
    files to <app_name> service rather than gunicorn.

    **WHY?**

    A VM may host multiple web apps. Using gunicorn as filename would be too generic
    if we will be hosting multiple apps

    References:

    * `Full django-gunicorn-nginx integration tutorial with debugging hints <https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu#step-10-configure-nginx-to-proxy-pass-to-gunicorn>`_
    * `Running multiple web apps <https://caterinadmitrieva.medium.com/serving-multiple-django-apps-on-second-level-domains-with-gunicorn-and-nginx-a4a14804174c>`_
    * `Incorporation of ssl certification <https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-20-04>`_

Configure Environment Variables
+++++++++++++++++++++++++++++++

By default, environment variables 

* Reading via os.environ:
  * This ensures that we are reading env variables exported in os system
* Boolean variables are read and should be evaluated as string
* A default value must be provided inside project settings if not read in environment

Sample that reflects all these rules are shown below

.. code-block:: python

    # in settings.py
    DEBUG = os.environ.get("DEBUG", "False") == "True"

.. important::

    Some **critical** values to be set in environment variables are:

    * SITE_ID 
        * Refer to Site list in django admin or query in shell
        * This is important for Oauth to also identify current site IP being used
        * Also important in utils/lambda functions: get_current_domain()
    * POSTGRES_*
        * This is dependency integrate postgresql server

.. note::

    If additional variables are needed to be added, just place them in .env files.
    See :ref:`Project Structure <project_structure_env_files>` for placement guide.

.. hint:: 

    See :ref:`_setup_environment_variables` to see how environment variables are read in the system

Handle Static Files
+++++++++++++++++++

An important component for production of django application is to load staticfiles correctly.

.. code-block:: shell

    # Double check static file loading by:
    # try toggling django app settings DEBUG=False
    python manage.py collectstatic
    python manage.py compress

.. tip::

    For any issues regarding compress, **ONLY wrap files in static folder**

    .. code-block:: html

        {% compress css %}
            <only files in static folder>
        {% endcompress %}

    Compress library essentially compresses files for app optimization

Setup network routing
---------------------

Bind Gunicorn WSGI Configuration
++++++++++++++++++++++++++++++++

.. code-block:: shell
    
    # bind gunicorn and django app with wsgi.conf
    # make sure manage.py runserver is not running
    # gunicorn will replace manage.py runserver
    .prod_venv/bin/gunicorn config.wsgi --bind 0.0.0.0:8000

    # open site to at port 8000 if no nginx/apache configuration yet to see if app is running

    # in the succeeding section, nginx/apache will refer to the gunicorn port for load balancing


.. tip::

    Add service to gunicorn to make sure that the system will run each restart of the system

    Create Gunicorn services for each app you will deploy in your server

.. code-block:: shell

    # /etc/systemd/system/<app_name>.socket
    [Unit]
    Description=gunicorn socket for <app_name> web app

    [Socket]
    ListenStream=/run/<app_name>.sock

    [Install]
    WantedBy=sockets.target

.. code-block:: shell

    # FOR NGINX /etc/systemd/system/<app_name>.service
    [Unit]
    Description=Gunicorn daemon for <app_name> web app
    Requires=<app_name>.socket
    After=network.target

    [Service]
    User=root
    Group=www-data
    WorkingDirectory=/path/to/working_directory
    Environment="ENV_FILE_DIR=/path/to/app/.envs/.production" #absolute_path
    # for nginx
    ExecStart=/path/to/venv/bin/gunicorn \
        --workers 3  \
        --bind unix:/run/<app_name>.sock config.wsgi:application \ 
        config.wsgi

    [Install]
    WantedBy=multi-user.target

.. code-block:: shell

    # debugging for integration may be tricky
    # some tips to check integration:

    sudo systemctl start <app_name>.socket
    sudo systemctl enable <app_name>.socket
    sudo systemctl start <app_name>.service #run app

    # check if sock file was created
    file /run/<app_name>.sock

    # to check status
    sudo systemctl status <app_name>.socket
    sudo systemctl status <app_name>.service

    # check logs
    sudo journalctl -u <app_name>

.. code-block:: shell

    # FOR APACHE /etc/systemd/system/<app_name>.service
    [Unit]
    Description=Gunicorn daemon for <app_name>  web app
    After=network.target

    [Service]
    User=root
    Group=www-data
    WorkingDirectory=/path/to/app
    Environment="DJANGO_SETTINGS_MODULE=config.settings.production"
    Environment="ENV_FILE_DIR=/path/to/app/.envs/.production"
    ExecStart=/bin/bash -c '/path/to/app/.prod_venv/bin/gunicorn config.wsgi --bind 0.0.0.0:8005'

    [Install]
    WantedBy=multi-user.target

.. tip::

    Isolate section testing by:

    * Running app
        * Test to run app using ```/path/to/venv/bin/python manage.py runserver```
    * Running binding gunicorn
        * Run app using gunicorn and check if accessible in IP&Port
    * Systemd
        * Run app using gunicorn and check if accessible in IP&Port

NGINX App Routing
+++++++++++++++++

Create and nginx conf for your system at: ```/etc/nginx/sites-enabled/<domain_name>```

.. code-block:: shell

    server {
        # routing
        server_name <domain_name>;
        listen 80;

        location = /favicon.ico { access_log off; log_not_found off; }

        # loading media files
        location /media/ {
            autoindex on;
            root /var/www/html/<app_name>/base/media;
        }

        # loading static files
        location /static/ {
            autoindex on;
            root /var/www/html/<app_name>/staticfiles;
        }

        location / {
            autoindex on;
            include proxy_params;
            # PRODUCTION
            # this will pass all traffic to appname socket
            proxy_pass http://unix:/run/<app_name>.sock;

            # TESTING / DEBUGGING
            #proxy_pass http://127.0.0.1:8000;
            #proxy_set_header Host $host;
            #proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            #proxy_set_header X-Forwarded-Proto $scheme;
            #proxy_redirect http://127.0.0.1:8000 http://foo.com;
        }

        # LET's ENCRYPT INTEGRATION
        # listen 443 ssl; # managed by Certbot
        # ssl_certificate /etc/letsencrypt/live/<domain_name>/fullchain.pem; # managed by Certbot
        # ssl_certificate_key /etc/letsencrypt/live/<domain_name>/privkey.pem; # managed by Certbot
        # include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
        # ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

        error_log /var/log/nginx/error.log;

    }

.. code-block:: shell

    # port allowance
    sudo ufw allow 'Nginx Full'

    # to restart nginx
    sudo service nginx restart

    # to check nginx status
    sudo service nginx status

    # to check running configuration files
    nginx -t

    # to check running configuration files and append include files
    nginx -T

Apache App Routing
+++++++++++++++++

.. code-block:: shell

    <VirtualHost *:80>
        ServerName <domain_name>
        Redirect permanent / https://<domain_name>
    </VirtualHost>

    <IfModule mod_ssl.c>
    <VirtualHost *:443>

        ServerName <domain_name>

            ProxyPass / http://127.0.0.1:8005/
            ProxyPassReverse / http://127.0.0.1:8005/

        <Directory /path/to/app/config>
            <Files wsgi.py>
                Require all granted
            </Files>
        </Directory>

        Alias /static/ /path/to/app/staticfiles/
            <Directory /path/to/app/staticfiles>
                    Require all granted
            </Directory>

        Alias /media/ /path/to/app/qmslib/media/
            <Directory /path/to/app/qmslib/media>
                    Require all granted
            </Directory>

        Redirect gone /favicon.ico
        RedirectMatch gone ^/apple-touch-icon

            ErrorLog /var/log/httpd/qmslib.error.log
            CustomLog /var/log/httpd/qmslib.acccess.log common


        <Directory /path/to/app/config>
            <Files wsgi.py>
                Require all granted
            </Files>
        </Directory>

        Alias /static/ /path/to/app/staticfiles/
            <Directory /path/to/app/staticfiles>
                    Require all granted
            </Directory>

        Alias /media/ /path/to/app/qmslib/media/
            <Directory /path/to/app/qmslib/media>
                    Require all granted
            </Directory>

        Redirect gone /favicon.ico
        RedirectMatch gone ^/apple-touch-icon

        ErrorLog /var/log/httpd/qmslib.error.log
        CustomLog /var/log/httpd/qmslib.acccess.log common

        Include /etc/letsencrypt/options-ssl-apache.conf

        SSLCertificateFile /etc/letsencrypt/live/<domain_name>/fullchain.pem
        SSLCertificateKeyFile /etc/letsencrypt/live/<domain_name>/privkey.pem
    </VirtualHost>
    </IfModule>

SSL Certification
+++++++++++++++++

.. code-block:: shell

    # installation dependencies
    sudo apt install certbot python3-certbot-nginx

    # obtaining ssl certification
    sudo certbot --nginx -d example.com -d www.example.com

    # for multiple 
    sudo certbot-auto -d one.example.com -d two.example.com -d three.example.com -d example.org