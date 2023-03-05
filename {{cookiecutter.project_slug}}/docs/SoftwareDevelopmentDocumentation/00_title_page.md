---
note_type: reference
writing_type: draft
toc: true
toc-own-page: true
listings-no-page-break: true
linkcolor: blue
date: Mar 06, 2023
title: 'Title'
subtitle: 'Insert subtitle here'
author: {{cookiecutter.author_name}} <{{cookiecutter.email}}>
titlepage: true
titlepage-background: '/home/sam/.pandoc/backgrounds/background7.pdf'
titlepage-text-color: '546f7a'
titlepage-rule-color: '546f7a'
page-background: '/home/sam/.pandoc/backgrounds/background7.pdf'
page-background-opacity: 0.15
header-includes:
- |
  ```{=latex}
  \usepackage{awesomebox}
  \usepackage{tcolorbox}

  \newtcolorbox{info-box}{colback=cyan!5!white,arc=0pt,outer arc=0pt,colframe=cyan!60!black}
  \newtcolorbox{warning-box}{colback=orange!5!white,arc=0pt,outer arc=0pt,colframe=orange!80!black}
  \newtcolorbox{error-box}{colback=red!5!white,arc=0pt,outer arc=0pt,colframe=red!75!black}
  ```
pandoc-latex-environment:
  noteblock: [note]
  tipblock: [tip]
  warningblock: [warning]
  cautionblock: [caution]
  importantblock: [important]
  tcolorbox: [box]
  info-box: [info]
  warning-box: [warn]
  error-box: [error]
---

# System Documentation

## {{cookiecutter.project_name}}

### Prepared by:

{{ cookiecutter.author_name }} | <{{ cookiecutter.email }}>

### Compiled and Completed:

*date*