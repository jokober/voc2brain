#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='Voc2brain',
      version='4.9a',
      description='Voc2brain is a simple flashcard software',
      author='Jonathan Kossick',
      author_email='dev.kossick@gmail.com',
      url='https://github.com/jokober/voc2brain',

      classifiers=[
                  "Development Status :: 3 - Alpha",
                  #"Development Status :: 4 - Beta",
                  #"Development Status :: 5 - Production/Stable",
                  "Environment :: X11 Applications :: Qt",
                  "Intended Audience :: Education",
                  "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
                  "Programming Language :: Python :: 2.7",
                  "Topic :: Education"
             ],

      install_requires=[
            'SQLAlchemy'
      ],

      packages=find_packages("voc2brain"),
      include_package_data=True,

      entry_points = {
        'gui_scripts': ['voc2brain=voc2brain:main'],

      }
     )


