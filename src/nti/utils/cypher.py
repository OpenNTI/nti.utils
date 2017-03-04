#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import base64
from itertools import cycle


def _XOR(text, key):
    """
    A TOY "cipher" that symmetrically obscures
    the `text` based `key`. Do not use this when
    security matters.
    """
    result = []
    key = cycle(key)
    for t in text:
        t = chr(ord(t) ^ ord(next(key)))
        result.append(t)
    return b''.join(result)

DEFAULT_PASSPHRASE = base64.b64decode('TjN4dFRoMHVnaHQhIUM=')


def make_ciphertext(plaintext, passphrase=DEFAULT_PASSPHRASE):
    """
    A trivial function that uses a toy "cipher" (XOR) to obscure
    and then base64 encode a sequence of bytes.
    """
    encoded = _XOR(plaintext, passphrase)
    result = base64.b64encode(encoded)
    return result


def get_plaintext(ciphertext, passphrase=DEFAULT_PASSPHRASE):
    """
    A trivial function that uses a toy "cipher" (XOR) to obscure
    a base64 encoded sequence of bytes.
    """
    result = base64.b64decode(ciphertext)
    result = _XOR(result, passphrase)
    return result
