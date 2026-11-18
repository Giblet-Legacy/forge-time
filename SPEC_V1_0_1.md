# SPEC V1.0.1 — forge-time (P16 Time), changes over SPEC 1.0.0

SPEC_V1_0_1.md — the one change P16 Time 1.0.1 makes to the signed SPEC 1.0.0.

Function:
    SPEC.md (1.0.0) is pinned by sha256 in the sealed sc/p16-time-v1.sc.json
    and is never edited. This file states only what 1.0.1 changes. Where
    it is silent, SPEC.md 1.0.0 applies unchanged.

Layer:    P16 — Time
Depends:  SPEC.md 1.0.0
Version:  SPEC 1.0.1
Licence:  MSL-1.0
Author:   James Gilbert (Giblets Forge)

---

## 1. No agreement check against the-full-stack (replaces one bullet of SPEC §5)

SPEC §5's bullet "Agreement with the foundation: if
`../the-full-stack/forge_core` is present, P16 and `forge_core` agree…"
is withdrawn. In its place:

- Nothing in this layer imports `forge_core` or looks for a
  `the-full-stack` folder (`test_never_reaches_the_full_stack`).

**Why:** James, 2026-11-18: "the forge stack was for reference only and
not meant to be a layer involved in the legacy program." P16's rules
were first taken from the-full-stack's `forge_core/canon.py`. That is
where they came from, not something they answer to. P16 itself is the
rule now.

## 2. What does not change

- `forge_time.py` and `seal_capsule.py`: not touched. Behaviour is
  identical, and the capsule's `spec_sha256` still names SPEC.md 1.0.0.
- The sealed capsule's `derived_from` and `inherits` fields stay as
  signed: they are history.
- The 1.0.0 test file is kept byte-identical at
  `archive/1.0.0/test_forge_time.py`. The 1.0.1 suite is
  `test_forge_time_v1_0_1.py`.

---

## Document control

- **SPEC 1.0.1** — 2026-11-18, by the VS Code AI on James's word ("yes
  in the order you stated", removing the the-full-stack ties). Not
  signed; 1.0.1 is not frozen until James says so.
