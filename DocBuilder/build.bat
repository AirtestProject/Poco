
:: build my doc together
rmdir /S /Q source\
mkdir source\
copy /Y ..\README.rst source\
copy /Y ..\README-CN.md source\
xcopy /Y /T ..\doc source\doc\
xcopy /Y /S /E ..\doc source\doc\

:: exclude undoc members
SET SPHINX_APIDOC_OPTIONS=members,show-inheritance
sphinx-apidoc -Me -o source/ ../poco ../poco/utils/simplerpc
sphinx-build -b html . ../doc-auto

:: copy readme.md to doc-auto
xcopy /Y /T ..\doc ..\doc-auto\source\source\doc\
xcopy /Y /S /E ..\doc ..\doc-auto\source\source\doc\

:: copy readme-built from .html to .md to ensure links are working well
copy /Y ..\doc-auto\source\README.html ..\doc-auto\source\README.rst
copy /Y ..\doc-auto\source\README-CN.html ..\doc-auto\source\README-CN.md
