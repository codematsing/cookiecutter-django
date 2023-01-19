# Automate env variables everytime virtualenv is activated

in [your_virtualenv_dir]/bin/postactivate:

``` shell
YOUR_ENV_VAR="hello world!"
```

# Automate env variables deactivation

in [your_virtualenv_dir]/bin/predeactivate:

``` shell
unset YOUR_ENV_VAR
```
