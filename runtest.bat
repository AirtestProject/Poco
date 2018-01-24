rd /s /q cover
del .coverage
nosetests test --with-coverage --cover-package ./poco --cover-html
pause
start cover/index.html

