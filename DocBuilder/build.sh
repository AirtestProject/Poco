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
