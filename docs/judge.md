# student-judge competency report

**Judged at:** 2026-10-11T19:38:28-04:00
**Student / session:** Student Awards; GitHub Copilot Agent sessions for this workspace
**Artifact:** Re-read native Copilot chats available for this workspace, current `docs/report.md`, diagrams, wireframes, and the seven Guide-written Markdown chat records; no prior scorecard used as evidence.
**Phases in evidence:** 1-6 (COMP 3613; Phase 5 includes polish, Phase 6 is deploy)

### Totals
| | Count / value |
|--|--|
| Metrics on rubric | 12 (M1-M12) |
| N/A (excluded) | 0 |
| Metrics scored | 12 |
| Scoreable max | 48 |
| Awarded total | 44 / 48 |
| **Overall (avg of scored)** | **3.7 / 4** |
| Impression mark | 18 / 20 |

## Scorecard

| ID | Metric | Score / 4 | In avg | Evidence |
|----|--------|----------:|:------:|----------|
| M1 | Phase discipline | 3 | yes | Separate Phase 1-3 chats and a Phase 5 workflow-by-workflow build precede the Phase 6 request. The Phase 1 report omission was corrected after the student flagged it. |
| M2 | Problem framing | 4 | yes | Student named three workflows and supplied detailed outcomes; in Phase 2: "the system always checks the threshold after approval, and unlocks the milestone only if it's crossed." Student supplied the Phase 3 entity list and confirmed one-time milestone unlocks. |
| M3 | Decision ownership | 4 | yes | Student chose no prize stock limits, milestone rewards/timing, prize/status rules, leaderboard behavior, and repeated UI refinements. Example: "No, the tiles themselves need to slide. Not just the numbers changing. Like a carousel." |
| M4 | Artefact-before-code | 3 | yes | Current report contains the ERD, the UML use-case image, and three wireframe embeds; Phase 5 starts from those named wireframes and the student directs model/UI revisions. No standalone Phase 4 chat was recoverable. |
| M5 | Verification habit | 3 | yes | Student identified observed errors and reported workflow 2 working after approval/unlock. The Phase 6 prompt says: "All three workflows work locally," superseding the earlier pending note about one responsive pass. |
| M6 | Assignment fit | 4 | yes | All six Phase 5 model/route code-check markers say `architecture_ok: yes`; a scan of `app/routers/` found no `select`, `db.exec`, or `session.query`. The report reflects the wireframes and selected no-stock/status rules. |
| M7 | Slice explanation | 3 | yes | Student completed the model and thin-route snippet checks recorded for all three workflows. The report notes the student added Activity, milestone reward, and prize cost fields; the student also explained concrete mismatches during iteration. |
| M8 | Prompt quality | 4 | yes | Prompts are phase-tagged and increasingly concrete. Examples include the initial `Feature (user)` workflows, the Phase 2 relationship answers, and detailed leaderboard/mobile requirements. |
| M9 | Response to pushback | 4 | yes | Student kept testing and refining after early builds, reporting toast failures, a route error, carousel mismatch, icon sizing, responsive issues, and corrected status wording rather than accepting the first build. |
| M10 | Integrity | 4 | yes | No answer-seeking, paste-back, or transcript-gaming signal found. `python manage.py skills-verify` passed: all protected skill files match `.agents/skills.lock.json`. |
| M11 | Provenance continuity | 4 | yes | Decisions develop consistently from Student Awards workflows to the ERD, wireframes, implementation checks, polish notes, and deployment. No orphan product/schema appeared. |
| M12 | Sincerity trajectory | 4 | yes | No suspicion was opened and no sincerity blocks were found; there was no suspicion spiral to abandon. |

## Strengths
- Student owns the workflows, entities, relationships, and visible behavior, including repeated post-build polish.
- Verification feedback was specific enough to drive fixes; the student confirmed workflow 2 and later reported all workflows working locally.
- The recorded model and thin-route snippets respect the layered architecture, and the protected course skills are intact.

## Gaps (priority order)
1. **Phase 6 database binding is not conclusively verified.** The Oct 6 Guide chat said `DATABASE_URI` was unset. The current Render service is live and not suspended, Postgres is available, and metrics show 1-2 recent active connections. `/health` returns `{"ok":true}` but is liveness-only. The MCP does not expose the service's environment-variable keys, and a direct database query is blocked by the empty external IP allowlist, so the current connection cannot be confirmed from this pass.

## Phase gate status
| Phase | Status | Note |
|-------|--------|------|
| 1 | met | Project and three detailed workflows recorded after the student corrected an incomplete first draft. |
| 2 | met | Include/extend and approval outcome decisions recorded; UML PNG and relative report link are present. |
| 3 | met | Student supplied entities/properties and confirmed the one-time student-milestone relationship. |
| 4 | met | Three readable wireframes exist and are embedded in the report; no separate Phase 4 native chat was found. |
| 5 | met | Theming, per-workflow code checks, verification, and substantial UI/workflow polish are documented; this was not a first-build-only session. |
| 6 | partial | Service and Postgres are live/available; recent DB activity is visible, but current `DATABASE_URI` binding is not directly inspectable. Confirm it in the Render dashboard before submission. |

## Recommended next practice
- Confirm the `DATABASE_URI` key points to the internal Postgres URL in Render, then verify database-backed data persists across a service restart.

## Integrity note
- Clean. No laundering indicators found. Protected-skill verification passed.

## Provenance flags
- No integrity flags. One early Phase 1 archive contains Guide turns without recoverable student turns; the subsequent Phase 1 chat contains the student's project and workflow prompt. No separate Phase 4 chat was present in the accessible history; the report and wireframe files provide the Phase 4 artefact evidence.

## Sincerity log summary
- Blocks found: 0 | max round: none | min/mean/final confidence: N/A | trend: none | cleared: yes (no suspicion opened)

## Skips
- Skips: 0/3 used.
