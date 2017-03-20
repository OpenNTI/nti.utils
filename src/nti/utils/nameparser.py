#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nameparser.config import prefixes
from nameparser.config import suffixes
from nameparser.config import Constants


def suffix_acronyms():
    return suffixes.SUFFIX_ACRONYMS


def suffix_not_acronyms():
    return suffixes.SUFFIX_NOT_ACRONYMS


def get_suffixes():
    return suffix_acronyms() | suffix_not_acronyms()


def all_suffixes():
    return get_suffixes() | suffix_acronyms() | suffix_not_acronyms()


def all_prefixes():
    return prefixes.PREFIXES


def constants(prefixes=(), extra_suffixes=()):
    not_acronyms = suffix_not_acronyms()
    acronyms = suffix_acronyms() | set(extra_suffixes)
    constants = Constants(prefixes=prefixes,
                          suffix_acronyms=acronyms,
                          suffix_not_acronyms=not_acronyms)
    return constants
