# Makefile help

![](https://img.shields.io/pypi/v/makefile-help)

This small package helps by generating colourful help for Makefiles.
- [Makefile help](#makefile-help)
    - [Why?](#why)
    - [Usage](#usage)
    - [Installation](#installation)

---
### Why?

I often store useful commands in Makefiles and then promptly forget them.

---
### Usage

At the top of a Makefile add the following (assuming makefile-help is installed in the current virtual env):

```
help: # @@Utils@@ Display help and exit
	python -m makefile_help
```

Comment each command with a description and optionally a section using `@@`  
The makefile_help script will then generate a help string.

![../makefile-help/image/demo.gif](https://raw.githubusercontent.com/simonwardjones/makefile-help/main/image/demo.gif)

---
### Installation

`pip install makefile-help`