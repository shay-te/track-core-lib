import os

import setuptools

import track_core_lib

from setuptools import find_namespace_packages, setup
from pip._internal.network.session import PipSession
from pip._internal.req import parse_requirements

dir_path = os.path.dirname(os.path.realpath(__file__))
install_reqs = parse_requirements(os.path.join(dir_path, 'requirements.txt'), session=PipSession)
requirements = []
try:
    requirements = [str(ir.req) for ir in install_reqs]
except:
    requirements = [str(ir.requirement) for ir in install_reqs]

packages1 = setuptools.find_packages()
packages2 = find_namespace_packages(include=['hydra_plugins.*'])
packages = list(set(packages1 + packages2))

with open('README.md', 'r') as fh:
    long_description = fh.read()

    setup(
        name='track_core_lib',
        version=track_core_lib.__version__,
        author='Shay Tessler',
        author_email='shay.te@gmail.com',
        description='manage track for users',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/shay-te/track-core-lib',
        packages=packages,
        license='MIT',
        classifiers=['Topic :: Software Development'],
        install_requires=requirements,
        include_package_data=True,
        python_requires='>=3.7',
    )
