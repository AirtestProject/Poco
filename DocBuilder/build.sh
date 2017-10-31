#!/usr/bin/env bash
rm -rf source/
mkdir source/
cp ../README.md source/
cp ../README-CN.md source/


# exclude undoc members
export SPHINX_APIDOC_OPTIONS=members,show-inheritance
sphinx-apidoc -Me -o source/ ../poco ../poco/utils/simplerpc
sphinx-build -b html . ../auto-doc

# copy readme.md to auto-doc
mkdir ../auto-doc/source/source
cp -r ../doc ../auto-doc/source/source

# copy readme-built from .html to .md to ensure links are working well
cp ../auto-doc/source/README.html ../auto-doc/source/README.md
cp ../auto-doc/source/README-CN.html ../auto-doc/source/README-CN.md
