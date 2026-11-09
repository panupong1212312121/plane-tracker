# Handoff brief template

Fill every section; show the user before invoking `/skill-creator`. Delete a section only if it is truly empty — never leave "TBD".

```markdown
# Skill brief: <kebab-slug>

**Verdict:** NO-SKILL | EXTEND <existing-name> | COMPANION (anchor: <locked-name>) | CREATE NEW
**Requested by:** <one line of the user's own words>

## Capability statement
<one sentence: what it does, to what input, producing what output.>

## Trigger phrases
- Fires on: "<phrase>", "<phrase>", "<phrase>"
- Never fires on: "<near-miss>", "<near-miss>" (those belong to <skill>)

## Boundary
- vs <nearest skill>: <one line>
- vs <second nearest>: <one line>

## Requirements
1. <observable behavior>
2. <observable behavior>
3. <observable behavior>

## Acceptance
1. <checkable outcome — a command, artifact, or state>
2. <checkable outcome>

## Lock & sync
- skills-lock.json: <new "local (built: …)" entry | refresh hash of <name>>
- Then: powershell -File scripts\sync-skills.ps1
```

## Filled example

```markdown
# Skill brief: skill-planner

**Verdict:** CREATE NEW
**Requested by:** "skill สำหรับพิจารณาว่าจะสร้างเพิ่มหรือขยาย skill เดิม"

## Capability statement
Given a capability idea, scan the skills inventory, classify overlap, and return a verdict plus a /skill-creator brief.

## Trigger phrases
- Fires on: "สร้าง skill สำหรับ X", "should I make a skill for this", "new skill or extend an existing one?"
- Never fires on: "write the skill" (/skill-creator), "why didn't my skills fire" (/skill-doctor)

## Boundary
- vs skill-creator: planner decides and stops; creator authors from the brief.
- vs skill-doctor: doctor grades from conversation evidence after the fact.

## Requirements
1. Inventory scan covers every canonical skill before any verdict.
2. Verdict is one of NO-SKILL / EXTEND / COMPANION / CREATE NEW, with the class of every near neighbor recorded.
3. Upstream-locked skills are never edited; the brief routes around them.

## Acceptance
1. User confirms the brief before /skill-creator is invoked.
2. skills-lock.json entry + sync-skills.ps1 run after authoring.
```
