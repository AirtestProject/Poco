#!/usr/bin/env bash

# exclude undoc members
# export SPHINX_APIDOC_OPTIONS=members,show-inheritance
# sphinx-apidoc -Me -o source/ ../poco ../poco/utils

# international multi-languages
sphinx-build -M gettext . _build/
sphinx-intl update -p _build/gettext -l zh_CN

sphinx-build -b html . ../doc-auto
