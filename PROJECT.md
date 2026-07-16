# PROJECT.md — NAIA Legends (tailored facts for /pm-run)

Generated from the project spec; retailor with /tailor when SPEC.md changes
materially. The PM never edits this file.

## Project

- **Name:** NAIA Legends — NFL Street–inspired 7v7 arcade football game
  (walls, exaggerated, fast) with real NAIA athletes via opt-in NIL licensing.
  Unreal Engine 5.8.
- **Product owner:** Brian (`@foleyb25`) — rules on `type:decision` issues,
  version exits, and merges.
- **Repo:** `NAIA-Legends/NAIA-Legends-Game`

## Documents

- Program spec (law): `SPEC.md`
- Active version spec (build target): `SPECS/SPEC_V0.md` — v0 "The Field"
- Workspace (product source): `UnrealProject/`
- Shared conventions: `UnrealProject/CLAUDE.md` (units, collision channels,
  Explicitly-OUT list, routing vocabulary)

## Consultation roster

| Agent | Role | Notes |
|---|---|---|
| `gd` | Game Designer / Feel Owner | consult before any mechanic is ticketed |
| `ge` | Gameplay Engineer | triage generalist for unclear routing |
| `aie` | AI Engineer | active v2–v7; FSM diagram in every report |
| `ta` | Tech Artist / Animation | budget guardrails (≤10 canned anims through v5) |
| `qa` | QA / Playtest Coordinator | **write exception:** may create `type:bug` issues directly (frontmatter grant); sweep its bugs into ticket_log each run (`source: 'qa_bug_sweep'`) |

## Routing table (mirror of SPEC.md §3.12 — source of truth is the spec)

| Feature area (prefix) | Primary | Co-consult |
|---|---|---|
| `movement.*` (locomotion, turbo, camera, input) | ge | gd (feel) |
| `passing.*`, `catching.*`, `ball.*` | ge | gd (feel targets) |
| `tackling.*`, `collision.*` | ge | ta (animations), aie (pursuit) |
| `ai.*` (pursuit, coverage, routes, rush) | aie | ge (integration) |
| `feel.*`, `tuning.*`, `playbook.*` | gd | ge (implementation notes) |
| `assets.*`, `animation.*`, `vfx.*`, `ui.*`, `audio.*` | ta | ge |
| `perf.*`, `tests.*`, `build.*`, `repro.*` | qa | ge |
| `pipeline.*` (repo, MCP stack, CI) | ge | qa |

## Labels & milestone

- `role:{pm|gd|ge|aie|ta|qa}` · `ver:{v0…v9}` ·
  `type:{feature|bug|tuning|decision|deferred}` — one label per dimension on
  every ticket.
- Active milestone: **v0 — The Field**

## Ledger

- Supabase project ref: `fotgjkolicebuklkidpa` (dedicated to this ledger)
- Tables per `docs/PM_DATASTORE.md`; upserts only (hook-enforced).

## Project-specific PM notes

- Program bets in risk order — never invert: core loop fun → street depth →
  real athletes → economics. No NIL spend before v6 exit; no monetization
  decision before v9 planning.
- The active spec's "Explicitly OUT" list is the scope checklist at ticket
  time; v0's list also lives in `UnrealProject/CLAUDE.md` §14.
- Perf floor 60 fps: v0 exit criterion and a standing regression check.
