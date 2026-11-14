# NOTES — forge-time (P16 Time)

NOTES.md — open questions, divergences and decisions for P16 Time.

Function:
    Records open questions, divergences from the foundation and
    decisions for P16. Owner: James.

## Open questions

- **Q1 — Sign off P16 at 1.0.0?** Built and green on the laptop (8/8).
  Not yet run on the S24. Raised 2026-11-14. Owner: James.
- **Q2 — Does the scp_id rule belong in P16?** It is here because it
  came with the time rules in the foundation's canon.py and James said
  yes to "the time and SCP-id rules" in one layer. It is a Declare (P1)
  rule; a later P1 layer could own it. Raised 2026-11-14. Owner: James.

## Divergences — from the foundation (forge_core/canon.py)

- **D1 — trailing newline.** The foundation's `ISO_UTC_RE` and
  `SCP_ID_RE` end in `$` and are used with `.match`, which accepts
  `"2026-11-14T17:00:00Z
"` and `"x/y-v1
"`. `parse_iso_utc` there
  still rejects the timestamp (strptime), but `sign.py`'s scp_id check
  accepts the id. P16 uses fullmatch. Fixing the foundation would mean
  changing patterns its own tests pin byte-for-byte to sign.py, so it
  is raised here rather than changed.

## Decisions

- Canonical JSON is not duplicated: P1 Envelope's `canonicalise` is
  byte-identical to the foundation's forge-c14n-1 (checked 2026-11-14).
  Decided by the VS Code AI on James's delegation.
- Module name `forge_time.py`, not `time.py`, which would shadow the
  standard library's `time`.
