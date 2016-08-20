#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import zope.deferredimport
zope.deferredimport.initialize()
zope.deferredimport.deprecatedFrom(
	"Moved to nti.property",
	"nti.property.property",
	"alias",
	"read_alias",
	"dict_alias",
	"dict_read_alias",
	"Lazy",
	"LazyOnClass",
	"CachedProperty",
	"readproperty",
	"_Lazy",
	"_CachedProperty",
	"annotation_alias")
