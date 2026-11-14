# forge-time — P16 Time

README.md — repository purpose and layer contract for P16 Time.

Function:
    This repository implements primitive layer P16 of the Forge Stack:
    the one timestamp format the stack signs (ISO 8601 UTC to the
    second, `YYYY-MM-DDTHH:MM:SSZ`) and the scp_id rule, each matched
    against the whole string. Taken from the foundation's
    forge_core/canon.py (JamesTheGiblet/the-full-stack); canonical JSON
    stays P1 Envelope's.

Layer:    P16 — Time
Depends:  none (standard library only)
Consumed: P17 Mediator; any layer or consumer that writes or checks a
          signed timestamp or an scp_id
Licence:  MSL-1.0
Author:   James Gilbert (Giblets Forge)
Status:   1.0.0 — frozen 2026-11-14 (SPEC.md 1.0.0), signed off by James

## Use

    import forge_time
    forge_time.utc_now()                              # '2026-11-14T18:00:00Z'
    forge_time.parse_iso_utc("2026-11-14T18:00:00Z")  # aware UTC datetime
    forge_time.is_iso_utc("2026-11-14T18:00:00Z
")  # False (whole string)
    forge_time.is_ratified_scp_id("forge-stack/primitive/p16-time-v1")  # True

## The primitive capsule

`sc/p16-time-v1.sc.json` declares this layer and pins SPEC.md's
SHA-256. James sealed it on 2026-11-14 (P3 Freeze v2, key_id
`did:key:z6MkkVnQM4mpSND1jMBLDScpuUFF9BJTMoxYykurXQY89pjn`,
the same key as the Legacy ledger). A later capsule is sealed the same way. To seal it with your key (P3 Freeze
v2, your passphrase-protected `~/.forge/key.pem`, passphrase asked for
and never stored):

    python seal_capsule.py sc/p16-time-v1.sc.json

## Tests

    python -m pytest -q

Needs the sibling checkouts ../envelope-layer, ../sign-layer,
../freeze-layer and ../record-layer (for seal_capsule.py). If
../the-full-stack is checked out too, P16 is also checked against the
foundation's forge_core.
