:: copy readme.md
mkdir source\
copy /Y ..\README.md source\

:: exclude undoc members
SET SPHINX_APIDOC_OPTIONS=members,show-inheritance
sphinx-apidoc -Me -o source/ ../poco ../poco/vendor
sphinx-build -b html . ../auto-doc

:: copy readme.md to auto-doc
xcopy /Y /T ..\doc ..\auto-doc\source\source\doc\
xcopy /Y /S /E ..\doc ..\auto-doc\source\source\doc\
