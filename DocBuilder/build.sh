cp ../README.md source/
sphinx-apidoc -Me -o source/ ../poco ../poco/vendor
sphinx-build -b html . ../auto-doc
