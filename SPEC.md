# SPEC — forge-time (P16 Time)

SPEC.md — the complete layer specification for P16 Time.

Function:
    This document is the authoritative specification for primitive
    layer P16 of the Forge Stack. It defines the one timestamp format
    the stack signs (ISO 8601 UTC to the second, with a literal Z) and
    the SCP identifier rule, as the foundation (JamesTheGiblet/
    the-full-stack, forge_core/canon.py) ratified them, so every layer
    and consumer can share one tested copy instead of its own regex.

Layer:     P16 — Time
Depends:   none (standard library only)
Consumed:  P17 Mediator; any layer or consumer that writes or checks a
           signed timestamp or an scp_id
Version:   SPEC 1.0.0
Licence:   MSL-1.0
Author:    James Gilbert (Giblets Forge)

---

## 1. Why P16

James (2026-11-14) shared the foundation's `forge_core/canon.py` and
asked for it to come into this stack "as primitive capsule … repo and
layer"; the GitHub repo `Giblet-Legacy/forge-time` ("P16 — Time: ISO
8601 UTC parse/format/validate") was created for it. Canonical JSON is
already P1 Envelope's (`envelope_v2.canonicalise`, byte-identical to
the foundation's forge-c14n-1), so P16 takes only what P1–P15 lack:
the timestamp format and the scp_id rule.

## 2. The formats

- **Timestamp:** `YYYY-MM-DDTHH:MM:SSZ` — four-digit year, two-digit
  month, day, hour, minute, second, a literal `T` and a literal `Z`;
  no fraction, no offset, nothing before or after.
- **scp_id:** one or more segments of `a-z`, `0-9` and `-`, separated
  by `/`, ending `-v` and one or more digits (for example
  `forge-stack/primitive/p16-time-v1`).

Both are matched against the **whole** string. The foundation's
regexes end in `$`, which also matches before a trailing newline, so
`"2026-11-14T17:00:00Z\n"` passes its `ISO_UTC_RE.match`; P16 uses a
full match and rejects it (NOTES D1).

## 3. API (`forge_time.py`)

1. `utc_now() -> str` — the current instant in the format.
2. `format_iso_utc(when: datetime) -> str` — a naive datetime is taken
   as UTC; an aware one is converted to UTC; fractions of a second are
   dropped (truncated, never rounded).
3. `parse_iso_utc(value: str) -> datetime` — an aware UTC datetime.
   Not a str → TypeError. Wrong shape, or a date or time that does not
   exist (`2026-02-30T00:00:00Z`, `…T24:00:00Z`) → ValueError.
4. `is_iso_utc(value) -> bool` — True exactly when `parse_iso_utc`
   would return; never raises.
5. `is_ratified_scp_id(value) -> bool` — the scp_id rule; never raises
   (a non-str is False).
6. `ISO_UTC_RE`, `SCP_ID_RE` — the compiled patterns, for callers that
   need them; use `fullmatch`.

`format_iso_utc` and `parse_iso_utc` round-trip: for every valid
string s, `format_iso_utc(parse_iso_utc(s)) == s`.

## 4. The primitive capsule

`sc/p16-time-v1.sc.json` declares this layer: `scp_id`
`forge-stack/primitive/p16-time-v1`, `inherits` the governance in
force (`forge-stack/governance-v6`), and a declaration naming the
layer, its module and this SPEC's SHA-256. It is committed unsigned;
the owner seals it with P3 Freeze v2 and his own key
(`python seal_capsule.py sc/p16-time-v1.sc.json`). The AI never signs.

## 5. Tests (test_forge_time.py)

- Formats: valid and invalid tables for both rules, including a
  trailing newline, lower-case `z`, offsets, fractions, impossible
  dates; whole-string match.
- `parse_iso_utc` errors (TypeError, ValueError); `is_*` never raise.
- `format_iso_utc`: naive as UTC, aware converted, fractions truncated;
  round-trip over a table.
- `utc_now` is in the format and within a second of the clock.
- Agreement with the foundation: if `../the-full-stack/forge_core` is
  present, P16 and `forge_core` agree on every string in the tables
  that has no trailing newline (skipped otherwise).
- The capsule's SPEC hash matches this file, and `seal_capsule.py`
  seals a copy with a throwaway key so that P3 v2 verifies it.

---

## Document control

- **SPEC 1.0.0** — 2026-11-14, by the VS Code AI on James's
  delegation ("fix all add as primitive capsule and intigrate as repo
  and layer"; "Yes, fill forge-time").
