set OUTPUT=../auto-doc
rmdir /S /Q source
rmdir /S /Q %OUTPUT%
sphinx-apidoc -o source/ ../poco
sphinx-build -b html . %OUTPUT%