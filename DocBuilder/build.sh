#!/usr/bin/env bash
rm -rf source/
mkdir source/
cp ../README.md source/


# exclude undoc members
export SPHINX_APIDOC_OPTIONS=members,show-inheritance
sphinx-apidoc -Me -o source/ ../poco ../poco/vendor
sphinx-build -b html . ../auto-doc

# copy readme.md to auto-doc
mkdir ../auto-doc/source/source
cp -r ../doc ../auto-doc/source/source
