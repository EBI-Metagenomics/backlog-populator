from setuptools import setup, find_packages
import os
import sys

_base = os.path.dirname(os.path.abspath(__file__))
_requirements = os.path.join(_base, 'requirements.txt')
_requirements_test = os.path.join(_base, 'requirements-test.txt')

version = '1.1.0'

install_requirements = []
with open(_requirements) as f:
    install_requirements = f.read().splitlines()

test_requirements = []
if "test" in sys.argv:
    with open(_requirements_test) as f:
        test_requirements = f.read().splitlines()

setup(name='emg-backlog-populator',
      version=version,
      description='Utility to sync MGnify backlog schema from ENA ',
      author='Miguel Boland',
      author_email='mdb@ebi.ac.uk',
      url='https://github.com/EBI-Metagenomics/backlog-populator',
      packages=find_packages(),
      install_requires=install_requirements,
      include_package_data=True,
      dependency_links=[
          'https://github.com/EBI-Metagenomics/emg-backlog-schema/tarball/master#egg=emg-backlog-schema-0.5.2',
          'https://github.com/EBI-Metagenomics/ebi-metagenomics-libs/tarball/master#egg=emg-libs-0.1.9'
      ],
      entry_points={
          'console_scripts': [
              'backlog_populator=src.update:main'
          ]
      },
      tests_require=test_requirements,
      test_suite="tests",
      setup_requires=['pytest-runner'],
      )
