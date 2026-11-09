# Deliverables and project files

Templates for the files every clone produces. Keep them short and current; a stale plan is worse than none.

## Contents
1. Project files (Memory, PLAN, Security, Optimization, agent)
2. Model routing and subagents
3. Fixes log
4. Client report
5. Pitch page (optional)
6. Launch readiness
7. Writing style

---

## 1. Project files

```
<project>/
  Memory.md          state, decisions, where things live (read first every session)
  PROJECT.md         intake answers
  PLAN.md            the plan, "blocked on owner" first
  Security.md        security rules and pre-launch checklist
  Optimization.md    speed targets, baseline, results
  agent.md           how agents work here: routing, hard rules, definition of done
  .env.local         secrets (git-ignored)
  docs/
    site-scan.md  feature-inventory.md  feature-parity.md  design-spec.md
    redirect-strategy.md  plugin-audit.md  local-environment.md
    site-fixes.md  launch-readiness.md  handoff-improvements.md
    qa/  report/  pitch/
  migration/
    input/   (raw exports, untouched)   private/ (PII, git-ignored, deleted after import)
    tools/   redirects/
  site/      (the build)
```

### Memory.md
```markdown
# Memory: <project>
Last updated: <date>

## State
What's built, what's in progress, what's blocked (one line each).

## Decisions
| Date | Decision | Why | Who decided |

## Where things live
URLs, ports, databases, commands to start/stop/reset, scripts that rebuild settings.

## Gotchas
Things that bit us and how to avoid them.
```

### PLAN.md
Sections: 0 Blocked on owner (table: need, why) · 1 Architecture · 2 Data mapping · 3 URL strategy and redirects · 4 Layout per page type and proposed improvements · 5 Feature parity checklist · 6 SEO · 7 Accessibility · 8 Performance · 9 Phases with owner (model/agent) per phase.

### Security.md
Process and data handling (read-only live site, PII rules, secrets) · platform hardening · accounts and auth · web server rules · commerce specifics · forms · extensions policy · backups · monitoring · pre-launch checklist with checkboxes. See `build-playbook.md` section 11 for defaults.

### Optimization.md
Baseline table (live site, method, date) · targets · methods applied · results table (new site, same method) · production requirements (host, cache, CDN).

### agent.md
Project one-liner · read-first order · model routing table · hard rules (numbered, from the ground rules) · repo layout · local stack · definition of done.

## 2. Model routing and subagents

| Work | Who | Examples |
|---|---|---|
| Architecture, decisions, all code, code review, security config, final report | Strongest model, main session | importer, redirect resolver, theme code, data model, plugin choices |
| Research, scanning, transcription, environment ops, visual QA, doc drafts | Mid-size model subagent | transcribe page set, compare screenshots, run imports the main session wrote |
| Bulk mechanical checks | Small fast model subagent | validate 30,000 redirects, link checks, log greps, alt text counts |

Rules:
- Anything a subagent produces that touches code or server config is reviewed by the main session before it's relied on.
- Each brief: goal, files, constraints, definition of done. The subagent doesn't know the conversation.
- Never two writers on the same files. Parallelize independent work only.
- A subagent's report is a claim; check the files or rerun the numbers before telling the user.

## 3. Fixes log

`docs/site-fixes.md`. Every fix gets a row in the same change that makes it, numbered in order, referenced in code comments as `fix N`. The client report is generated from it.

```markdown
# Site fixes

Everything that was wrong on the old site, or broke during the build, and what was done.

## Navigation and layout
| # | What was wrong | Why it mattered | What we did | Status |
|---|---|---|---|---|
| 1 | No "Skip to content" link | Keyboard users tab through the whole header on every page | Skip link is the first thing on every page | Fixed |

## Problems found during the build
| # | What broke | What we did | Status |
|---|---|---|---|
| B1 | Logo spilled over the menu bar | Sized through the theme's own setting | Fixed |
```

Sections that work well: Navigation and layout · Product pages · Category pages · Search · Cart and checkout · Content · SEO · Accessibility · Speed · Security · Problems found during the build. Statuses: Fixed · Partly fixed · Needs owner · Won't fix (with why).

## 4. Client report

Audience: the business owner. Format: a document (Word/Google Doc/PDF) or a page.

1. Summary (five lines: what was built, the headline numbers, what's needed to launch).
2. Before and after: screenshots of home, category, product, checkout, phone.
3. Speed table: old vs new, same method, with a note on test conditions.
4. What shoppers will notice (plain list).
5. Search engine fixes (titles, structured data, redirects: "33,126 old addresses tested, all reach the right page in one step").
6. Accessibility fixes.
7. **What the old platform still does better.** Be honest: built-in features the new site needs extensions or work for, things not yet verified. This builds trust and avoids launch surprises.
8. Extensions/plugins used, free or paid, monthly cost.
9. What the owner needs to provide or decide (accounts, keys, approvals).
10. Launch plan.
11. Appendix: the full fixes log.

Use real numbers from the QA files, not estimates.

## 5. Pitch page (optional)

A single HTML page when the user is selling the work: hero with the headline numbers, side-by-side sliders (old vs new) per page type with fix numbers, speed comparison, "what the new site wins" and "what it doesn't win" sections, plugins and costs, what's needed from the owner, timeline. Light background, real screenshots, nothing invented. Build a standalone version with images inlined so it can be emailed.

## 6. Launch readiness

`docs/launch-readiness.md`:
- Tested flows (with dates and results).
- Pre-launch tasks (ours).
- Items that need the owner's permission or accounts: DNS, live payment keys, email domain authentication, analytics access, Search Console, hosting purchase, legal text approval, decisions still open.
- Launch-day steps in order, with who does each: freeze old admin, final delta import, switch gateway to live, DNS (TTL lowered a day earlier), edge redirects on, smoke test, sitemap submitted, monitoring on.
- Rollback plan.
- First two weeks: daily 404 log and order checks.

## 7. Writing style

Owners read these, so:
- Plain words, short sentences, concrete numbers. "33,126 old addresses checked; all reach the right page in one step."
- Say what was wrong, why it mattered to customers, what was done.
- No hype, no filler, no "seamless", "robust", "leverage", "elevate", no triplets of adjectives.
- Don't claim what wasn't tested. Say "not yet verified on the production host" when that's the truth.
- Run an avoid-AI-writing pass if a skill for it is installed.
