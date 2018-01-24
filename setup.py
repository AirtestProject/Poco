# coding=utf-8

from setuptools import setup, find_packages
from pip.req import parse_requirements

import poco


# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements.txt', session=False)

# reqs is a list of requirement
reqs = [str(ir.req) for ir in install_reqs if ir.req]

setup(
    name='pocoui',
    version=poco.__version__,
    keywords="poco",
    description='Poco cross-engine UI automated test framework.',
    packages=find_packages(),
    include_package_data=True,
    install_requires=reqs,
    license='Apache License 2.0',

    author='adolli, adolli, lxn3032, gzliuxin',
    author_email='adolli@163.com, adollixiang@gmail.com, lxn3032@corp.netease.com, gzliuxin@corp.netease.com',
)
