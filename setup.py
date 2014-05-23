from distutils.core import setup

setup(name='commasearch',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Find amicus curiae in briefs.',
      url='https://github.com/tlevine/friendly_brief',
      py_modules = 'friendly_brief',
      tests_require = ['nose'],
      version=__version__,
      license='AGPL',
      classifiers=[
          'Programming Language :: Python :: 3.4',
      ],
)
