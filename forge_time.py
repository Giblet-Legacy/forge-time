"""
forge_time.py — P16 Time: the stack's one timestamp format and the scp_id rule

Function:
    Implements SPEC.md 1.0.0. The only timestamp the stack signs is ISO
    8601 UTC to the second with a literal Z (YYYY-MM-DDTHH:MM:SSZ); an
    scp_id is a-z0-9- segments joined by "/" and ending -vN. Both match
    the whole string (the foundation's `$` patterns also accepted a
    trailing newline: NOTES D1). Pure functions, standard library only,
    no I/O. Taken from the foundation's forge_core/canon.py (JamesTheGiblet/
    the-full-stack); canonical JSON stays P1 Envelope's.

Public API:
    1. utc_now() -> str
    2. format_iso_utc(when) -> str
    3. parse_iso_utc(value) -> datetime
    4. is_iso_utc(value) -> bool
    5. is_ratified_scp_id(value) -> bool
    ISO_UTC_RE, SCP_ID_RE (use fullmatch)

Layer:    P16 — Time
Depends:  none (standard library)
Spec:     SPEC.md 1.0.0
Version:  1.0.0
Licence:  MSL-1.0
Author:   James Gilbert (Giblets Forge)
"""

import re
from datetime import datetime, timezone

ISO_UTC_RE = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
SCP_ID_RE = re.compile(r"[a-z0-9-]+(?:/[a-z0-9-]+)*-v[0-9]+")
_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


# ---------------------------------------------------------------------------
# 1. utc_now
# ---------------------------------------------------------------------------
def utc_now():
    return format_iso_utc(datetime.now(timezone.utc))


# ---------------------------------------------------------------------------
# 2. format_iso_utc
#    Naive is taken as UTC; aware is converted; fractions are dropped.
# ---------------------------------------------------------------------------
def format_iso_utc(when):
    if not isinstance(when, datetime):
        raise TypeError(f"when must be a datetime, got {type(when).__name__}")
    when = when.astimezone(timezone.utc) if when.tzinfo else when.replace(tzinfo=timezone.utc)
    return when.strftime(_FORMAT)


# ---------------------------------------------------------------------------
# 3. parse_iso_utc
#    Not a str -> TypeError; wrong shape or an impossible date or time
#    -> ValueError. Returns an aware UTC datetime.
# ---------------------------------------------------------------------------
def parse_iso_utc(value):
    if not isinstance(value, str):
        raise TypeError(f"value must be a str, got {type(value).__name__}")
    if not ISO_UTC_RE.fullmatch(value):
        raise ValueError(f"value must be ISO 8601 UTC, YYYY-MM-DDTHH:MM:SSZ: {value!r}")
    try:
        return datetime.strptime(value, _FORMAT).replace(tzinfo=timezone.utc)
    except ValueError:
        raise ValueError(f"no such date or time: {value!r}") from None


# ---------------------------------------------------------------------------
# 4. is_iso_utc
#    True exactly when parse_iso_utc would return; never raises.
# ---------------------------------------------------------------------------
def is_iso_utc(value):
    try:
        parse_iso_utc(value)
        return True
    except (TypeError, ValueError):
        return False


# ---------------------------------------------------------------------------
# 5. is_ratified_scp_id
#    Whole-string match; a non-str is False.
# ---------------------------------------------------------------------------
def is_ratified_scp_id(value):
    return isinstance(value, str) and SCP_ID_RE.fullmatch(value) is not None
