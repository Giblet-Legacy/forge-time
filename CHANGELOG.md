# CHANGELOG — forge-time (P16 Time)

CHANGELOG.md — build history for P16 Time, latest entry at top.

Function:
    Records the Good / Bad / Ugly of every build step for this layer.
    Updated at every sign-off. The format never changes shape, even
    when a section is empty.

## [Unreleased]

### Good

- `forge_time.py`, `SPEC.md` 1.0.0, `test_forge_time.py` (8 tests,
  run red first): the stack's timestamp format and scp_id rule as one
  tested primitive, from the foundation's forge_core/canon.py. Whole-
  string matching; impossible dates and times are ValueError; non-str
  input is TypeError; `is_*` never raise. Agrees with the foundation on
  every shared case.
- `sc/p16-time-v1.sc.json`: the layer's primitive capsule, pinning
  SPEC.md's SHA-256, inheriting forge-stack/governance-v6; unsigned
  until James seals it with `seal_capsule.py` (P3 Freeze v2, his key).
- Built on James's delegation ("fix all add as primitive capsule and
  intigrate as repo and layer").

### Bad

- The foundation's patterns end in `$`, so its `ISO_UTC_RE.match` and
  `SCP_ID_RE.match` accept a trailing newline (NOTES D1). P16 does not;
  the foundation is not changed by this layer.

### Ugly

- (none)
