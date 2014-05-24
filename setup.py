import os
from distutils.core import setup

setup(name='friendly_brief',
      author='Thomas Levine',
      author_email='_@thomaslevine.com',
      description='Find amicus curiae in briefs.',
      url='https://github.com/tlevine/friendly_brief',
      packages = ['friendly_brief'],
      scripts = [os.path.join('bin', 'friendly-brief')],
      install_requires = ['unidecode>=0.04.16'],
      tests_require = ['nose'],
      version='0.0.1',
      license='AGPL',
      classifiers=[
          'Programming Language :: Python :: 3.4',
      ],
)
