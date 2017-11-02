#!/usr/bin/env bash

# build my doc together
rm -rf source/
mkdir source/
cp ../README.rst source/
cp ../README-CN.md source/
cp -r ../doc source/
cp -r ../doc source/

# exclude undoc members
export SPHINX_APIDOC_OPTIONS=members,show-inheritance
sphinx-apidoc -Me -o source/ ../poco ../poco/utils/simplerpc
sphinx-build -b html . ../doc-auto

# copy readme.md to doc-auto
mkdir ../doc-auto/source/source
cp -r ../doc ../doc-auto/source/source

# copy readme-built from .html to .md to ensure links are working well
cp ../doc-auto/source/README.html ../doc-auto/source/README.rst
cp ../doc-auto/source/README-CN.html ../doc-auto/source/README-CN.md
