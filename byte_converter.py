#!/usr/bin/env python

"""
Bytes-to-human / human-to-bytes converter.
Based on: http://goo.gl/kTQMs
Working with Python 2.x and 3.x.

Author: Giampaolo Rodola' <g.rodola [AT] gmail [DOT] com>
License: MIT

Modified by Sergi Lange-Soler
"""

SYMBOLS = ('B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB')


def bytes2human(n, format='%(value).1f %(symbol)s'):
    """
    Convert n bytes into a human readable string based on format.
    see: http://goo.gl/kTQMs
    """
    n = int(n)
    if n < 0:
        raise ValueError("n < 0")
    prefix = {}
    for i, s in enumerate(SYMBOLS[1:]):
        prefix[s] = 1 << (i+1)*10
    for symbol in reversed(SYMBOLS[1:]):
        if n >= prefix[symbol]:
            value = float(n) / prefix[symbol]
            return format % locals()
    return format % dict(symbol=SYMBOLS[0], value=n)
