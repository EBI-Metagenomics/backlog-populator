from distutils.core import setup

setup(name='MGnify Backlog populator',
      version='0.1',
      description='Utility to sync MGnify backlog schema from ENA ',
      author='Miguel Boland',
      author_email='mdb@ebi.ac.uk',
      url='https://github.com/EBI-Metagenomics/backlog-populator',
      packages=['backlog-populator', 'distutils.command'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      requires=['dateutil', 'PyYAML', 'django', 'backlog']
      )