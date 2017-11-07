#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

import sys
import types
import unittest

from zope.dottedname import resolve as dottedname


def create_module(location):
    try:
        __import__(location)
    except ImportError:
        module = types.ModuleType(str(location), "Created module")
        sys.modules[location] = module


class TestInterfaces(unittest.TestCase):

    def test_import_schema(self):
        dottedname.resolve('nti.utils.schema')

    def test_import_cypher(self):
        create_module('nti')
        create_module('nti.common')
        create_module('nti.common.cypher')
        dottedname.resolve('nti.utils.cypher')

    def test_import_ldap(self):
        create_module('nti')
        create_module('nti.common')
        create_module('nti.common.model')
        dottedname.resolve('nti.utils.ldap')

    def test_import_oauthkeys(self):
        create_module('nti')
        create_module('nti.common')
        create_module('nti.common.model')
        dottedname.resolve('nti.utils.oauthkeys')
