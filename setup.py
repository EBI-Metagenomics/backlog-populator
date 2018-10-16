from setuptools import setup

setup(name='MGnify Backlog populator',
      version='1.0.0',
      description='Utility to sync MGnify backlog schema from ENA ',
      author='Miguel Boland',
      author_email='mdb@ebi.ac.uk',
      url='https://github.com/EBI-Metagenomics/backlog-populator',
      packages=['backlog_populator'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      requires=['dateutil', 'PyYAML', 'django', 'backlog'],
      entry_points={
          'console_scripts': [
              'backlog_populator=backlog_populator.update:main'
          ]
      }
      )
