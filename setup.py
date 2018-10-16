from setuptools import setup, find_packages
import os
_base = os.path.dirname(os.path.abspath(__file__))
_requirements = os.path.join(_base, 'requirements.txt')

with open(_requirements) as f:
    install_requirements = f.read().splitlines()


setup(name='emg-backlog-populator',
      version='1.0.2',
      description='Utility to sync MGnify backlog schema from ENA ',
      author='Miguel Boland',
      author_email='mdb@ebi.ac.uk',
      url='https://github.com/EBI-Metagenomics/backlog-populator',
      packages=find_packages(),
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      install_requires=install_requirements,
      dependency_links = ['http://github.com/EBI-Metagenomics/emg-backlog-schema.git#egg=emg-backlog-schema'],
      entry_points={
          'console_scripts': [
              'backlog_populator=backlog_populator.update:main'
          ]
      }
      )
