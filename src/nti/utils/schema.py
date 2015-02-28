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
	"Moved to nti.dataserver.core.schema",
	"nti.dataserver.core.schema",
	"DataURI"
)

zope.deferredimport.deprecatedFrom(
	"Moved to nti.schema.fieldproperty",
	"nti.schema.fieldproperty",
	"aq_base",
	"absolute_import",
	"IAcquirer",
	"FieldProperty",
	"FieldPropertyStoredThroughField",
	"AdaptingFieldProperty",
	"AcquisitionFieldProperty",
	"AdaptingFieldPropertyStoredThroughField",
	"UnicodeConvertingFieldProperty",
	"createFieldProperties",
	"createDirectFieldProperties")

zope.deferredimport.deprecatedFrom(
	"Moved to nti.schema.interfaces",
	"nti.schema.interfaces",
	"InvalidValue",
	"BeforeSetAssignedEvent",
	"BeforeDictAssignedEvent",
	"BeforeTextAssignedEvent",
	"BeforeObjectAssignedEvent",
	"BeforeSequenceAssignedEvent",
	"BeforeTextLineAssignedEvent",
	"BeforeCollectionAssignedEvent",
	"BeforeSchemaFieldAssignedEvent",
	"IVariant",
	"IFromObject",
	"IBeforeSetAssignedEvent",
	"IBeforeTextAssignedEvent",
	"IBeforeDictAssignedEvent",
	"IBeforeSequenceAssignedEvent",
	"IBeforeTextLineAssignedEvent",
	"IBeforeIterableAssignedEvent",
	"IBeforeContainerAssignedEvent",
	"IBeforeCollectionAssignedEvent",
	"IBeforeSchemaFieldAssignedEvent",
	"find_most_derived_interface")

zope.deferredimport.deprecatedFrom(
	"Moved to nti.schema.vocabulary",
	"nti.schema.vocabulary",
	"_SimpleTerm",
	"_SimpleVocabulary",
	"_CountryVocabulary",
	"_ICountryAvailability",
	"CountryTerm",
	"CountryVocabularyFactory")

zope.deferredimport.deprecatedFrom(
	"Moved to nti.schema.schema",
	"nti.schema.schema",
	"EqHash",
	"schemadict",
	"SchemaConfigured",
	"PermissiveSchemaConfigured")

zope.deferredimport.deprecatedFrom(
	"Moved to nti.schema.subscribers",
	"nti.schema.subscribers",
	"before_object_assigned_event_dispatcher")

zope.deferredimport.deprecatedFrom(
	"Moved to nti.schema.field",
	"nti.schema.field",
	'Bool',
	'Date',
	'Dict',
	'Choice',
	'Decimal',
	'DateTime',
	'Datetime',
	'DecodingValidTextLine',
	'DictFromObject',
	'EqHash',
	'FieldValidationMixin',
	'Float',
	'FrozenSet',
	'HTTPURL',
	'IndexedIterable',
	'Int',
	'InvalidValue',
	'Iterable',
	'List',
	'ListOrTuple',
	'ListOrTupleFromObject',
	'Number',
	'Object',
	'ObjectBase',
	'ObjectLen',
	'PermissiveSchemaConfigured',
	'SchemaConfigured',
	'Set',
	'Text',
	'TextLine',
	'Timedelta',
	'Tuple',
	'TupleFromObject',
	'UnicodeConvertingFieldProperty',
	'UniqueIterable',
	'ValidBytes',
	'ValidBytesLine',
	'ValidChoice',
	'ValidDatetime',
	'ValidRegEx',
	'ValidRegularExpression',
	'ValidSet',
	'ValidText',
	'ValidTextLine',
	'ValidURI',
	'Variant',
	'_ValueTypeAddingDocMixin',
	'_do_set')
