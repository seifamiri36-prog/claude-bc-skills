# business-central-development — changes against upstream

**Upstream:** [Mindrally/skills](https://github.com/Mindrally/skills) › `business-central-development/SKILL.md`,
licensed under Apache License 2.0 (copy in `LICENSE-Apache-2.0.txt`). The unmodified upstream
text is kept in `UPSTREAM-ORIGINAL.md` as a diff baseline.

**This fork (corrected 18 Aug 2026):** four upstream statements were wrong for AL. Each was
checked against Microsoft Learn before it was changed.

| # | Upstream said | Corrected to | Why (source) |
|---|---|---|---|
| 1 | "Implement try-catch blocks" | AL has no try/catch — use `[TryFunction]` (consume the return value!) or `if not Codeunit.Run(...)`; no DB writes inside a try function | MS Learn: *Handling errors using Try methods*; on-prem default `DisableWriteInsideTryFunctions` |
| 2 | "Use Error, Message, and Confirm" without caveat | Guard interactive calls with `if GuiAllowed() then` — `Confirm` throws in job queue / web service sessions | MS Learn: *Job queue* / client callback restriction |
| 3 | "PascalCase for public members, camelCase for private" | PascalCase throughout; quoted names with spaces are the BC standard; AL has no camelCase convention (3 of 23,370 standard fields start lowercase) | measured against a BC 28 data-model extract |
| 4 | Page example without `ApplicationArea` | `ApplicationArea = All` on the page (controls inherit); page/report **extensions** do not inherit | MS Learn: *ApplicationArea property*; linter rules PTE0008 / AS0062 |

Additional edits: "object-oriented" → "object-based" (AL has no classes/inheritance; interfaces
exist from BC 16), an ID-range note on the examples, the rule "look standard names up instead of
recalling them", and links to the relevant Microsoft Learn pages.

One upstream line ("Use AL's assertion system…") is kept unchanged and marked as *not verified*.

**Maintenance:** if you refresh this skill from upstream (`npx skills add Mindrally/skills --skill
business-central-development`), diff the result against `UPSTREAM-ORIGINAL.md` and re-apply the
corrections above — an upstream refresh overwrites them.
