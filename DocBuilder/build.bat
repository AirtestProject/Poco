set OUTPUT=../auto-doc
rmdir /S /Q source
rmdir /S /Q %OUTPUT%
sphinx-apidoc -Me -o source/ ../poco ../poco/vendor
sphinx-build -b html . %OUTPUT%