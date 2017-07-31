from distutils.core import setup
from pip.req import parse_requirements


# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements.txt', session=False)
# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs if ir.req]
print(reqs)
setup(
    name='poco',
    version='0.0.1',
    py_modules=['poco'],
    packages=['poco'],
    install_requires=reqs,
)
