#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='Voc2brain',
      version='4.9',
      description='Voc2brain is a simple flashcard software',
      author='Jonathan Kossick',
      author_email='dev.kossick@gmail.com',
      #url='https://www.python.org/sigs/distutils-sig/',

      install_requires=[
            'setuptools'
      ],

      packages=find_packages("."),
      py_modules=['voc2brain'],
      include_package_data=True,

      entry_points = {
        'gui_scripts': ['voc2brain=voc2brain:main'],

      }
     )