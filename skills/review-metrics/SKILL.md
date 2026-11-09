---
name: review-metrics
description: Record the two delivery-review metrics from the AI-native SDLC playbook — review-latency (branch first-commit → first /code-review verdict) and escape-ratio (defects caught before merge ÷ defects escaping to production) — by appending an append-only metric block to the ticket file after every /code-review run, and marking escapes when /investigate-first confirms a production defect a gate should have caught. Use when closing a ticket right after /code-review, when the user asks for review metrics, baseline data, "ตัวชี้วัดรีวิว", or when a /monitoring + /investigate-first triage confirms an escaped defect. Not the review itself (/code-review), not sensors (/monitoring), not acceptance proof (/verify-and-stop).
metadata:
  version: "1.0"
  author: local
---

# Review Metrics

The review loop produces evidence for free — if someone writes it down at the moment it happens. Timestamps are write-once: a missed recording is unrecoverable, so this skill's only job is capture-at-the-moment plus one-line reporting.

## Metric definitions (source of truth)

- **review-latency (leading):** first commit timestamp on the ticket's branch (from `git log` — never hand-entered) → timestamp of the first `/code-review` verdict. Target: minutes.
- **escape-ratio (lagging):** defects/vulns caught before merge (code-review + tests) ÷ defects confirmed by `/investigate-first` to have escaped a gate to production. Reported per release.

## Process

### 1. Record after every /code-review run (append-only)

Append one block to the bottom of the ticket file (issue-tracker conventions), then commit continues:

```yaml
## Review metrics
- review_started_at: <first commit timestamp on branch>
- reviewed_at: <now>
- latency_minutes: <reviewed_at − review_started_at>
- verdict: PASS | FIX (findings by severity: CRITICAL/HIGH/MEDIUM/LOW/NIT)
- escaped: false
```

One block per review round. Never edit a past block — a correction is a new block that notes the correction.

### 2. Mark escapes (evidence-gated)

When `/investigate-first` confirms a production defect that a gate should have caught: append a block to the ticket that produced the change with `escaped: true`, which gate missed (code-review / tests / verify-and-stop), and the `/monitoring` event ID. No event ID = not proven — same bar as `/monitoring`'s own guardrail.

### 3. Report on request (or every 10 tickets)

One line: median review-latency over the window + escape count vs caught count. Missing data is reported as missing — never estimated.

## Guardrails

- Never fabricate or back-fill timestamps; absent data is reported as absent.
- Append-only: editing past metric blocks is a finding, not a fix.
- This skill never judges code — `/code-review` owns the verdict; this skill records it.
- Solo-branch exception (per flow.md): when the user ordered work straight to main, record `review_started_at` from the ticket's claim timestamp instead and note the deviation inside the block.
