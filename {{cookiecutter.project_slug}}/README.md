# {{cookiecutter.project_name}}

{{ cookiecutter.description }}

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

{%- if cookiecutter.open_source_license != "Not open source" %}

License: {{cookiecutter.open_source_license}}
{%- endif %}

# Custom Set-up

## Project Preparations:

* Contracts Detail Form:
  * Ask for Personal Information
  * Valid ID
    * ID No
    * Date / Place Issued
  * TIN
  * PhilHealth Number
  * Bank Details
    * Savings Account
    * Photo of Front Face
  * CV
  * Github details
  * Pubkeys
  * SMTP Settings
* Request for dev server credentials
* Request for VPN

## Documentation
* Refer to [Sphinx Documentation](./docs/getting-started.rst) for getting started guidelines
* Getting started guidelines tackle:
  * How to clone repository
  * Proper virtualenv setup
  * Installation of dependencies
  * Creation of database
  * Running of site; and,
  * Running of documentation (side-by-side with system)