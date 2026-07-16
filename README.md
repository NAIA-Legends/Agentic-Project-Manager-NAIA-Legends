# Agentic Project Manager — NAIA Legends

The **tailored PM pipeline for [NAIA Legends](https://github.com/NAIA-Legends/NAIA-Legends-Game)**,
an NFL Street–inspired 7v7 arcade football game (Unreal Engine 5.8) featuring
real NAIA athletes via opt-in NIL licensing.

This is a project fork of the generic
[Agentic-Project-Manager](https://github.com/foleyb25/Agentic-Project-Manager)
template. The tailoring (this repo's delta over the template) was generated
from the game's `SPEC.md`: `config/apm.yaml` + `agents/roles/*.md`. It lives
as the `AgenticProjectManager/` submodule in the game repo, and CI runs it
there (`.github/workflows/pm.yml`).

Template improvements flow in via the upstream remote:

```bash
git remote add template git@github.com:foleyb25/Agentic-Project-Manager.git
git fetch template && git merge template/main
```

## How this instance works

One **PM agent** orchestrates: it reads `SPEC.md` and the active version spec
(`SPECS/SPEC_V0.md`), consults advisory role agents, writes deduplicated
GitHub Issues (labels `role:* / ver:v0–v9 / type:*`, milestone
**v0 — The Field**), logs every action to the Supabase ledger, and replies on
every thread that mentions **`@pm`**. It runs nightly, on `@pm` comment
events, and on manual dispatch. Humans (Brian + collaborators) are the
execution layer — agents never write code or PRs.

## Provisioned agents — and why (SPEC.md §3)

| Agent | Charter | Why the spec provisions it |
|---|---|---|
| **pm** (`agents/pm.md`) | Orchestrator; sole GitHub Issue/Milestone writer and sole ledger writer; enforces scope ("Explicitly OUT" → `type:deferred`), dedup, and the `@pm` reply protocol | §3.1 — the pipeline's coordinator; program bet order is enforced here (never invert: fun → depth → athletes → economics) |
| **gd** — Game Designer / Feel Owner (`agents/roles/gd.md`) | Feel targets, tuning values, playbook data, catch-resolution rules; consulted **before any mechanic is ticketed** — its design notes become acceptance criteria | §3.2 — program bet #1 is "the core loop is fun"; v1 movement and v3 passing are feel-gated; owns the Decision #2 recommendation (contested-catch model) |
| **ge** — Gameplay Engineer (`agents/roles/ge.md`) | Pawn control, ball flight, catch/tackle resolution, input, camera, match FSM, pipeline/CI; also the cheap **triage generalist** for unclear routing | §3.3 — carries the UE-approach research burden (risk: Brian's core stack is TS/Python; policy: Blueprint-first where sane, C++ where it counts) |
| **aie** — AI Engineer (`agents/roles/aie.md`) | Per-pawn FSMs: pursuit (v2), routes (v3), coverage + rush-timer (v4), later laterals/blocking/defense; every consult returns an FSM diagram + StateTree-vs-custom recommendation | §3.4, active v2–v7 — exit criteria demand *stable, readable, fair* AI ("pursuit never oscillates/jitters"); FSM diagrams go verbatim into tickets |
| **ta** — Tech Artist / Animation (`agents/roles/ta.md`) | Asset pipeline (Fab/Mixamo sourcing, retargeting), animation setup, materials, VFX/UI — with **budget guardrails**: ≤10 canned animations through v5, buy-don't-author until the tone decision | §3.5, v2+ light until v6 — mitigates the "animation cost balloons" program risk; art direction is blocked on Decision #1 (tone) at v6 |
| **qa** — QA / Playtest Coordinator (`agents/roles/qa.md`) | Regression checklists, automation tests, perf profiling, exit-criterion test protocol (including the v4 "stranger" session). Holds the **one scoped write exception**: may file `type:bug` issues directly (config-granted; PM dedup-reconciles post-hoc) | §3.6 — 60 fps is program law from v0 onward; v4 is the honest kill/pivot gate and needs a structured protocol; repro context degrades fast, so bug-filing speed wins |

**Deliberately not provisioned** (SPEC.md §3.7): BE (backend/platform) and
BizOps arrive at v8 (NIL portal, campaigns); attorney/NAIA-relationship/
monetization calls are **human-only, never agents**.

All five consultants are **advisory-only and read-only** (allowlists enforced
in `config/apm.yaml`, not by prompt promises). They read the game code, the
specs, and the web; their entire output is a JSON report
(`schemas/consultation.json`) that makes the PM's tickets smart.

### Consultation routing (mirror of SPEC.md §3.12)

| Feature area | Primary | Co-consult |
|---|---|---|
| `movement.*` | ge | gd |
| `passing.*`, `catching.*`, `ball.*` | ge | gd |
| `tackling.*`, `collision.*` | ge | ta, aie |
| `ai.*` | aie | ge |
| `feel.*`, `tuning.*`, `playbook.*` | gd | ge |
| `assets.*`, `animation.*`, `vfx.*`, `ui.*`, `audio.*` | ta | ge |
| `perf.*`, `tests.*`, `build.*`, `repro.*` | qa | ge |
| `pipeline.*` | ge | qa |

One taxonomy serves routing, dedup fingerprints, and ledger notes; the
machine-readable form (which actually drives the PM) is `config/apm.yaml`.

## Running it

```bash
cd AgenticProjectManager          # inside the game repo
uv sync
uv run apm run --trigger manual   # one full PM run (local claude login)
uv run apm run --dry-run          # inspect the composed prompt
uv run apm consult ge "pipeline.ci: sanity-check the workflow"
uv run apm ledger get sync_cursor scope=repo
uv run apm bootstrap              # labels + 'v0 — The Field' milestone (idempotent)
```

Ledger backend: **supabase** (service key in CI secrets only; humans read via
Studio). Cost knobs, ledger backends, and architecture: see the
[template README](https://github.com/foleyb25/Agentic-Project-Manager#readme)
and `docs/` (`PM_DATASTORE.md` for the ledger protocol, `setup.md` for the
one-time checklist).

Local secrets (e.g. the Supabase keys): `cp .env.example .env` and fill it in
— the CLI auto-loads it, shell-exported vars always take precedence, and the
file is gitignored. CI ignores `.env` entirely (Actions secrets instead).

**Design rule inherited from the template: protocol in Python, judgment in
prompts.** Retailor with `/tailor` only when `SPEC.md` changes materially —
and commit the result here, then bump the submodule pin in the game repo.
