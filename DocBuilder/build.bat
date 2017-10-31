:: copy readme.md
rmdir /S /Q source\
mkdir source\
copy /Y ..\README.md source\
copy /Y ..\README-CN.md source\

:: exclude undoc members
SET SPHINX_APIDOC_OPTIONS=members,show-inheritance
sphinx-apidoc -Me -o source/ ../poco ../poco/utils/simplerpc
sphinx-build -b html . ../auto-doc

:: copy readme.md to auto-doc
xcopy /Y /T ..\doc ..\auto-doc\source\source\doc\
xcopy /Y /S /E ..\doc ..\auto-doc\source\source\doc\

:: copy readme-built from .html to .md to ensure links are working well
copy /Y ..\auto-doc\source\README.html ..\auto-doc\source\README.md
copy /Y ..\auto-doc\source\README-CN.html ..\auto-doc\source\README-CN.md
