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

"""Lightweight symbolic test framework."""

__author__ = "stefan.bucur@epfl.ch (Stefan Bucur)"


import logging
import re
import struct
import sys
import traceback
import symbex


class SymbolicTest(object):
    """Base class for symbolic tests"""

    def __init__(self, replay_assgn=None):
        self.replay_assgn = replay_assgn

    def getInt(self, name, default, max_value=None, min_value=None):
        if self.replay_assgn:
            if name not in self.replay_assgn:
                logging.info("Key '%s' not found in assignment. Using default '%s'." % (name, default))
                return default
            return self.replay_assgn[name]
        elif not (max_value is None and min_value is None):
            return symbex.symint(default, name, max_value, min_value)
        else:
            return symbex.symint(default, name)

    def getString(self, name, default, max_size=None, min_size=None, ascii=False):
        if not isinstance(default, basestring):
            raise ValueError("Default value must be string or unicode")

        if self.replay_assgn:
            if name not in self.replay_assgn:
                logging.info("Key '%s' not found in assignment. Using default '%s'." % (name, default))
                return default
            return self.replay_assgn[name]
        elif not (max_size is None and min_size is None):
            value = symbex.symsequence(default, name, max_size, min_size)
        else:
            value = symbex.symsequence(default, name)

        if ascii:
            symbex.assumeascii(value)

        return value
    # supply
    def killstate(self,status,messages):
        symbex.killstate(status,messages)

    # todo 
    def Assert(self,expression):
        symbex.Assert(expression)

    def concretize(self, value):
        if self.replay_assgn:
            return value
        
        return symbex.concrete(value)

    def setUp(self):
        """Called once before the test execution."""
        pass

    def runTest(self):
        pass


def runSymbolic(symbolic_test, max_time=0, interactive=False, **test_args):
    """Runs a symbolic test in symbolic mode"""

    test_inst = symbolic_test(**test_args)
    test_inst.setUp()

    is_error_path = False
    symbex.startconcolic(max_time, not interactive)

    try:
        test_inst.runTest()
    except:
        if interactive:
            traceback.print_exc()
        is_error_path = True
    finally:
        if not interactive:
            symbex.endconcolic(is_error_path)
