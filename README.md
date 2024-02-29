# Forked Cookiecutter Django

Powered by [Cookiecutter](https://github.com/cookiecutter/cookiecutter), Cookiecutter Django is a framework for jumpstarting
production-ready Django projects quickly.

-   Documentation: <https://cookiecutter-django.readthedocs.io/en/latest/>
-   See [Troubleshooting](https://cookiecutter-django.readthedocs.io/en/latest/troubleshooting.html) for common errors and obstacles

# Usage

* Interactive Approach
``` shell
$ cookiecutter https://github.com/codematsing/cookiecutter-django
```

* Config File Approach
``` shell
$ wget -O cookiecutter_config.yaml https://raw.githubusercontent.com/codematsing/cookiecutter-django/master/cookiecutter.yaml
$ vim cookiecutter_config.yaml # change values
$ cookiecutter https://github.com/codematsing/cookiecutter-django --no-input --config-file api_cookiecutter.yaml
```