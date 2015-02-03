#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilities having to do with property definitions and access.

.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import operator

from zope.annotation.interfaces import IAnnotations

def annotation_alias(annotation_name, annotation_property=None, default=None, 
					 delete=False, delete_quiet=True, doc=None):
	"""
	Returns a property that is a read/write alias for
	a value stored as a :class:`zope.annotation.interface.IAnnotations`.

	The object itself may be adaptable to an IAnnotations, or a property
	of the object may be what is adaptable to the annotation. The later is intended
	for use in adapters when the context object is what should be adapted.

	:keyword bool delete: If ``True`` (not the default), then the property can be used
		to delete the annotation.
	:keyword bool delete_quiet: If ``True`` and `delete` is also True, then the property
		will ignore key errors when deleting the annotation value.
	:keyword str annotation_property: If set to a string, it is this property
		of the object that will be adapted to IAnnotations. Most often this will
		be ``context`` when used inside an adapter.
	"""

	if doc is None:
		doc = 'Alias for annotation ' + annotation_name

	factory = IAnnotations
	if annotation_property:
		factory = lambda self: IAnnotations( getattr( self, annotation_property ) )

	fget = lambda self: factory(self).get(annotation_name, default)
	fset = lambda self, nv: operator.setitem( factory(self), annotation_name, nv )
	fdel = None
	if delete:
		def fdel(self):
			try:
				del factory(self)[annotation_name]
			except KeyError:
				if not delete_quiet:
					raise

	return property( fget, fset, fdel,
					 doc=doc )

import zope.deferredimport
zope.deferredimport.initialize()
zope.deferredimport.deprecatedFrom(
	"Moved to nti.common",
	"nti.common.property",
	"alias",
	"read_alias",
	"dict_alias",
	"dict_read_alias",
	"Lazy",
	"LazyOnClass",
	"CachedProperty",
	"readproperty",
	"_Lazy",
	"_CachedProperty")
