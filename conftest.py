"""
conftest.py — pytest path setup for P16 Time

Function:
    Puts this directory and the sibling P1, P2, P3 and P7 directories
    (../envelope-layer, ../sign-layer, ../freeze-layer, ../record-layer)
    on sys.path, located from this file rather than the working
    directory, so the tests run from any directory. forge_time.py itself
    imports no layer; the siblings are for seal_capsule.py (P3 Freeze v2
    and P7 Record v2). Contains no functions.

Layer:    P16 — Time
Licence:  MSL-1.0
Author:   James Gilbert (Giblets Forge)
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_PARENT = os.path.dirname(_HERE)

for _p in [os.path.join(_PARENT, d) for d in ("envelope-layer", "sign-layer", "freeze-layer", "record-layer")] + [_HERE]:
    if _p not in sys.path:
        sys.path.insert(0, _p)
