#!/usr/bin/env python3

from distutils.core import setup

long_description = """touchgui is a Python module which implements a
basic touchgui for pygame"""

setup (name="touchgui",
       version="2.0",
       py_modules = ['touchgui', 'touchguipalate', 'touchguiconf'],
       description="touchgui is a Python module which implements a basic touchgui for pygame",
       author="Gaius Mulley",
       author_email="gaius.southwales@gmail.com",
       url="http://floppsie.comp.glam.ac.uk/touchgui",
       license="GPL license",
       platforms="UNIX",
)
