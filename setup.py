from setuptools import setup, find_packages

setup(name='emg-backlog-populator',
      version='1.0.2',
      description='Utility to sync MGnify backlog schema from ENA ',
      author='Miguel Boland',
      author_email='mdb@ebi.ac.uk',
      url='https://github.com/EBI-Metagenomics/backlog-populator',
      packages=find_packages(),
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      requires=['dateutil', 'PyYAML', 'django', 'backlog'],
      entry_points={
          'console_scripts': [
              'backlog_populator=backlog_populator.update:main'
          ]
      }
      )
