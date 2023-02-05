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

# Git Branch Standard

[Reference](https://towardsdatascience.com/how-to-structure-your-git-branching-strategy-by-a-data-engineer-45ff96857bb)

![Git Branch Image](https://miro.medium.com/max/786/1*q_w5pcaH7WT1larRd631jQ.webp)
