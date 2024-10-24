#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 EPFL.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Setup script for the Chef Python symbolic test library."""

__author__ = "stefan.bucur@epfl.ch (Stefan Bucur)"

from distutils.core import setup, Extension

def buildExtSymbex():
    return Extension('symbex', ['src/symbexmodule.cc',
                                'src/ConcolicSession.cc',
                                'src/S2EGuest.cc',
                                'src/SymbolicUtils.cc'])
                     

setup_flags = dict(
    name="ChefSymTest",
    version='0.1',
    description="The Chef symbolic test library",
    author="Stefan Bucur",
    author_email="stefan.bucur@epfl.ch",
    url="http://dslab.epfl.ch",
    ext_modules=[buildExtSymbex()]
)

setup(**setup_flags)