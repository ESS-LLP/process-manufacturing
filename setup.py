# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import re
from ast import literal_eval


with open('requirements.txt') as r:
	install_requires = r.read().strip().split('\n')

# get version from __version__ variable in process_manufacturing/__init__.py
_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('process_manufacturing/__init__.py', 'rb') as f:
	version = str(literal_eval(_version_re.search(f.read().decode('utf-8')).group(1)))

setup(
	name='process_manufacturing',
	version=version,
	description='Process Manufacturing',
	author='earthians',
	author_email='info@earthianslive.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
