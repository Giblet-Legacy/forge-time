"""
seal_capsule.py — seal a layer's primitive capsule with the owner's key

Function:
    Freezes and signs an unsigned .sc.json capsule in place with P3
    Freeze v2 (document_sha256, then P2's Ed25519 signature), so P3's
    verify_frozen_capsule accepts it. The key is the owner's
    passphrase-protected PEM, loaded by P7 Record v2; the passphrase is
    asked for with getpass and never stored, logged or passed on the
    command line. The file is replaced atomically and written with LF.
    The AI that builds a layer never runs this: sealing is the owner's.

    python seal_capsule.py sc/p16-time-v1.sc.json [--key ~/.forge/key.pem]

Public API:
    1. seal(path, private_key) -> dict
    2. main(argv=None) -> int

Layer:    P16 — Time (tooling; P17 Mediator uses it too)
Depends:  P3 Freeze v2, P7 Record v2 (sibling checkouts)
Spec:     SPEC.md 1.0.0 §4
Licence:  MSL-1.0
Author:   James Gilbert (Giblets Forge)
"""

import argparse
import getpass
import json
import os
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
for _d in ("envelope-layer", "sign-layer", "freeze-layer", "record-layer"):
    _p = os.path.join(os.path.dirname(_HERE), _d)
    if _p not in sys.path:
        sys.path.insert(0, _p)

import freeze_v2  # noqa: E402
import record_v2  # noqa: E402


# ---------------------------------------------------------------------------
# 1. seal
#    Freeze and sign the capsule at path; write it back atomically, LF.
# ---------------------------------------------------------------------------
def seal(path, private_key):
    with open(path, encoding="utf-8") as f:
        capsule = json.load(f)
    sealed = freeze_v2.freeze_capsule(capsule, private_key)
    if not freeze_v2.verify_frozen_capsule(sealed, private_key.public_key()):
        raise RuntimeError("sealed capsule does not verify; nothing written")
    folder = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(prefix=os.path.basename(path) + ".", suffix=".tmp", dir=folder)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(sealed, indent=2, ensure_ascii=False) + "\n")
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
    return sealed


# ---------------------------------------------------------------------------
# 2. main
# ---------------------------------------------------------------------------
def main(argv=None):
    p = argparse.ArgumentParser(description="Seal a layer's primitive capsule with your key (P3 Freeze v2).")
    p.add_argument("capsule")
    p.add_argument("--key", default=os.path.join(os.environ.get("FORGE_HOME", os.path.expanduser("~/.forge")),
                                                 "key.pem"))
    args = p.parse_args(argv)
    try:
        key = record_v2.load_private_key(args.key, getpass.getpass("key passphrase: "))
        sealed = seal(args.capsule, key)
    except (OSError, ValueError, RuntimeError) as e:
        print(f"seal failed: {e}", file=sys.stderr)
        return 1
    print(f"sealed {args.capsule}  document_sha256={sealed['document_sha256'][:16]}…")
    return 0


if __name__ == "__main__":
    sys.exit(main())
