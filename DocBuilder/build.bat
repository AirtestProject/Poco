
:: 需要先build一次，不然下面无法自动gettext
sphinx-build -b html . ../doc-auto

:: international multi-languages
sphinx-build -M gettext . _build/
sphinx-intl update -p _build/gettext -l zh_CN

sphinx-build -b html . ../doc-auto
