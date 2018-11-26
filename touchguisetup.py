#!/usr/bin/env python

from distutils.core import setup

long_description = """touchgui is a Python module which implements a
basic touchgui for pygame"""

setup (name="touchgui",
       version="1.0",
       py_modules = ['touchgui', 'palate'],
       description="touchgui is a Python module which implements a basic touchgui for pygame",
       author="Gaius Mulley",
       author_email="gaius@gnu.org",
       url="http://floppsie.comp.glam.ac.uk/touchgui",
       license="GPL license",
       platforms="UNIX",
)
