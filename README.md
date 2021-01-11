# Pretty Makefile help

This small package helps by generating colourful help for Makefiles.

Why? I often store useful commands in Makefiles and then promptly forget them.

### Usage

At the top of the makefile add the following (assuming makefile-help is installed in the current virtual env):

```
help: # @@Utils@@ Display help and exit
	python -m makefile_help
```

Comment each command with a description and optionally a section using `@@`  
The makefile_help script will then generate a help string.


### Installation

```sh
pip install makefile-help
```