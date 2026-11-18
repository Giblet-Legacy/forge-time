# Forge Stack Context — P16 Time

CLAUDE.md — Context briefing for AI assistants working in this repository.

Function:
    Instructs the AI assistant on the strict architectural rules of the
    Forge Stack. Do not hallucinate external frameworks. Reason strictly
    within these boundaries.

## The Immutable Rule
Never rewrite a primitive. Add a layer. Once forge_time.py is frozen, a
change is a forge_time_v2.py over it, after a SPEC_V2.md describes it.

## Dual-Device Workflow
We build on an S24 (Termux) and a laptop (VS Code). State is confirmed,
never assumed. Always use LF line endings. Good/Bad/Ugly CHANGELOG,
latest at top. British English (-ise).

## Header Discipline
Every file has a top header paragraph explaining its function. Every
function has a numbered header (e.g. `# 1. utc_now`).

## P16 Architecture Specifics
- Standard library only; imports no layer. seal_capsule.py (tooling)
  uses P3 Freeze v2 and P7 Record v2.
- the-full-stack (JamesTheGiblet) is reference only, never a layer or
  a dependency (James, 2026-11-18; SPEC_V1_0_1.md). P16's rules came
  from its forge_core.canon. Never import it, test against it or treat
  it as authority. NOTES D1 is history.
- Canonical JSON is P1 Envelope's, not P16's.
- The AI never seals the capsule; the owner does.
