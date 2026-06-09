# TDD with LLM Agents — Workflow Guide

> This guide defines a collaborative test-driven development workflow between a human developer
> and an LLM agent. It is a living document — sections are updated as the workflow matures.
> It is written to be read and followed by both the human and the LLM.

---

## Governing Principle

**Offload extraneous cognitive load to the LLM. Keep intrinsic load with the user.
Deliberately add germane load to build lasting fluency.**

This principle governs every design decision in this workflow. When in doubt about who should
do something, apply this test: *does this action require understanding, judgment, or authorship
of intent?* If yes, it belongs to the user. If it is formatting, translation, boilerplate,
or bookkeeping, it belongs to the LLM.

### The Three Loads

| Load | What it is | Who owns it |
|---|---|---|
| **Intrinsic** | The inherent difficulty of specifying and understanding the system | **User** |
| **Extraneous** | Incidental work: syntax, formatting, boilerplate, state-tracking | **LLM** |
| **Germane** | Effort that builds durable understanding and fluency | **User**, deliberately added by LLM |

### Intrinsic Load — What Always Stays with the User

The following are never delegated to the LLM, even when it would be faster:

- Writing behavioral specifications in prose
- Authoring examples and edge cases (even rough ones)
- Writing pseudocode when intrinsic load is present (see Pseudocode Ladder)
- Writing the test logic — assertions, cases, and the intent behind each test
- Making design decisions when tradeoffs are present
- Understanding why a component works, not just that it does
- Signing off on all specifications before tests are written
- Documentation prose and narrative intent

### Extraneous Load — What the LLM Always Owns

- Translating pseudocode and prose specs into working code
- Writing test file boilerplate and framework wiring — never test logic
- Formatting, linting, and style compliance
- Finalizing and polishing examples provided by the user
- Maintaining the workbench, log, reports, debt tracker, and mindmap
- Organizing and archiving files per established conventions

---

## Foundations

### Directory Layout

```
/src                         — source code
/tests                       — all test files
/workflow                    — workbench, log, reports, debt tracker, technique menu, mindmap
/workflow/reports            — one report per completed handshake
/archive                     — settled or superseded work
run_tests.py                 — test runner (see below)
pytest.ini                   — pytest configuration
```

### Starter Files

The following files must exist before the first session. Templates for all of them are
provided in the project repository. Do not begin development until these are in place.

| File | Purpose |
|---|---|
| `/workflow/workbench.md` | Current project state — fill in Project Conventions before first session |
| `/workflow/log.md` | Append-only session and event log |
| `/workflow/debt.md` | Technical debt tracker |
| `/workflow/techniques.md` | Desirable difficulty prompts, organized by technique type |
| `/workflow/mindmap.mm.md` | Conceptual mindmap — seed with the project's central idea |
| `run_tests.py` | Test runner script |
| `pytest.ini` | pytest configuration |
| `src/__init__.py` | Source package root |
| `tests/test_placeholder.py` | Placeholder test — delete once first real component is built |

### Test Runner

Tests are run via `run_tests.py` at the project root.

```bash
python run_tests.py                          # Run all tests
python run_tests.py --component <name>       # Run tests for one component
python run_tests.py --verbose                # Run all tests with verbose output
```

The `--component` flag takes the component name and resolves to
`tests/test_<component_name>.py`. The runner exits with pytest's exit code, so it
integrates cleanly with any CI setup.

### File Locations

- Test files: `test_<component_name>.py` in `/tests`
- Source files: `<component_name>.py` in `/src`
- Reports: `/workflow/reports/report_<YYYY-MM-DD>_<component>.md`
- Archives: `/archive/<component_name>_<YYYY-MM-DD>/`
- All workflow meta-files are committed to version control alongside source code.

### Tooling

Language and test framework are Python and pytest. Any additional conventions (import
style, type annotation policy, docstring format) are agreed at project start, recorded
in the workbench under Project Conventions, and never assumed by the LLM.

### Sources of Truth

- The workbench is the canonical source of truth for current project state.
- The mindmap is the canonical source of truth for conceptual project structure.

---

## Session Rituals

Every session has two rituals: one at the start, one at the end. These externalize project
state so the user never has to re-orient the LLM from scratch. The LLM may also update
the workbench and log at any other time if the user asks.

### First Session — Initialization Ritual

The first session is different from all subsequent ones because no workbench, log, or
mindmap content exists yet. The initialization ritual replaces the hello ritual for
session one only.

1. The LLM confirms that all starter files are in place (see Foundations — Starter Files).
2. The LLM asks the user to fill in Project Conventions in the workbench if not already done:
   language, test framework, any naming conventions.
3. The LLM asks the user to seed the mindmap with the project's central idea.
4. The LLM writes the first log entry: `session:initialized`.
5. The LLM asks: "What is the first thing you want to build?" Development begins.

### Hello Ritual

Triggered at the start of every session after the first.

1. The LLM reads the workbench and log.
2. The LLM offers a brief summary: what was last worked on, what is pending, what the next action is.
3. The user confirms, corrects, or redirects.
4. Development begins.

### Goodbye Ritual

Triggered when the user says **"Ok, Goodbye!"** or any clear signal that the session is ending.

1. The LLM updates the workbench to reflect current state.
2. The LLM appends a session-close entry to the log.
3. The LLM proposes any mindmap updates for conceptual work introduced this session.
4. The user reviews and confirms or revises mindmap proposals.
5. The LLM runs the GC pass (see Garbage Collection).
6. The LLM surfaces the desirable difficulty prompts for the session (see Desirable Difficulties).
7. Session ends.

---

## Part I — The Development Loop

*This is where intrinsic load lives. The loop is the core of the workflow.*

---

### Tests First

Every component begins with tests. No implementation is written until tests exist and are
confirmed by the user. The sequence within a component always follows:

```
prose spec  →  examples & edge cases  →  pseudocode (if applicable)  →  tests  →  implementation  →  review
```

**Who does what:**

The user writes the behavioral specification — what the component should do, in prose.
The user provides examples and edge cases, even if rough or incomplete.
The user writes all test logic: the assertions, the cases, and the intent behind each one.
The LLM writes test file boilerplate and framework wiring around the user's test logic.
The LLM never generates test cases on its own. If the user asks it to, it nudges instead.
The LLM flags gaps — missing edge cases, ambiguous behavior — as questions, not as tests it writes itself.
Both the user and the LLM see test failures together. Both can propose fixes; the user decides.

**Before writing tests, there is a spec-in-prose step.** The user writes — in plain language —
what the component does, what it does not do, and at least two concrete examples. This is not
optional. It is the primary intrinsic-load moment of the loop, and it comes before anything else.

**How many tests:** Many. The LLM actively encourages the user to think of more — surfacing
the coverage heuristic (happy path, boundary conditions, failure modes, type/shape contracts)
as a prompt, not as a list it fills in. The LLM asks: "What happens if X is empty? What if
Y is negative?" The user answers by writing the test. "Enough" is a judgment call made
together, after the checklist has been walked through with the user.

**Tests are never optional.** Unit, component, and integration tests are all written before
implementation. The granularity depends on the component; the requirement does not.

---

### Conversational Style

Development is a dialogue. Neither party issues instructions to the other; both propose,
question, and respond. The LLM does not proceed past a decision point without explicit user
assent.

**Question types the LLM uses:**

- *Clarifying intent:* "What should happen when X receives an empty input?"
- *Challenging an assumption:* "This spec implies Y; is that intentional, or should Z be handled separately?"
- *Offering alternatives:* "One approach is A; another is B — A is simpler, B handles future case C. Worth discussing."

**Suggestions vs. questions are kept strictly separate.** A question asks; it does not lead.
A suggestion is explicitly flagged — "Suggestion:" — so the user always knows whether they
are being asked for their view or offered a recommendation. Questions are never used to
smuggle in suggestions.

**Feedback from the LLM follows a loose heuristic:** observation → reasoning → suggestion → tradeoff.
This is a heuristic, not a required structure. The point is that a suggestion never arrives
without the reasoning that supports it, and the cost of taking it.

**Turn-taking is explicit.** After the LLM asks a question or gives feedback, it waits.
It does not answer its own questions. When it is the user's turn to write a spec, provide
examples, or make a decision, the LLM names that explicitly: "Your turn: what should the
component do when X?" Intrinsic load is handed to the user by name.

**Exit condition:** The conversation closes on explicit user assent. The LLM may suggest
that the spec feels complete and ask if the user agrees. The user confirms. This is the
only valid exit from conversation into test-writing.

---

### The Two-Way Handshake

Every piece of development — new features, refactors, bugfixes, documentation — goes through
a handshake. The handshake is the unit of collaborative work. It begins with a proposal from
either party, ends with user assent, and produces a committed entry in the log.

**Either party can initiate** a handshake. The user proposes a feature; the LLM notices a
needed refactor and proposes it. Both are valid. Both follow the same process.

**The flow of a handshake:**

```
Proposal (user or LLM)
  → Conversation — clarify, challenge, offer alternatives
  → Spec in prose (user writes)
  → Pseudocode if intrinsic load is present (user writes, LLM translates)
  → Tests (user writes logic, LLM writes boilerplate, LLM nudges toward coverage)
  → Implementation (LLM writes, user reviews)
  → Report (LLM writes)
  → Review & assent (user closes the handshake)
```

This flow is a guide, not a rigid state machine. Steps can overlap, repeat, or be revisited.
What is fixed: the spec always precedes tests, tests always precede implementation,
and the user always closes the handshake.

**Parking and cancellation:** A handshake can be paused or abandoned at any point.
When this happens, the LLM logs the current state and the reason so it can be resumed or
reviewed later. Parking is symmetric — either party can call it.

---

## Part II — Persistent Artifacts

*These files externalize project state. Their purpose is to ensure the user never has to
hold bookkeeping in working memory.*

---

### Workbench and Work Log

Two files, two purposes. The workbench is mutable: it reflects current state.
The log is append-only: it records what happened.

**The Workbench** (`/workflow/workbench.md`) contains:

```
# Workbench

## Project Conventions
[Language, test framework, naming conventions — established at project start]

## Current Focus
[What is being worked on right now — one handshake at a time]

## Done
[Completed components and handshakes, most recent first]

## Pending
[Queued work, ordered by priority]

## Blocked
[Items waiting on a decision, resource, or clarification]

## Open Decisions
[Design decisions not yet made, with context]

## Next Action
[The single next concrete step]
```

**The Log** (`/workflow/log.md`) records entries in this format:

```
[timestamp] | [actor: user | LLM] | [handshake state] | [artifact touched] | [decision or event]
```

Example entries:
```
2024-06-09 | LLM  | handshake:opened        | workbench.md | Proposed refactor of replay buffer indexing
2024-06-09 | user | handshake:spec-complete  | —            | Confirmed spec: buffer should evict by priority, not recency
2024-06-09 | LLM  | session:closed          | workbench.md | Updated workbench; goodbye ritual complete
```

---

### Reports

After implementation is complete, the LLM writes a report. The report is the readable record
of what was built, how, and why. It lives in `/workflow/reports/`.

**A report covers:**

- What changed and why
- Key design decisions made during the handshake
- Methods and patterns used
- Pseudocode → code translation, if applicable (what the user wrote, what it became)
- Test summary: what is covered, what edge cases are tested
- Open risks or known limitations

**Verbosity:** Reports are useful only if they are read. The LLM keeps them signal-dense.
If a decision was trivial, it is not in the report. If the pseudocode translation was
straightforward, a single line suffices. The report is not a log of effort; it is a record
of consequential choices.

---

### Project Mindmap

The mindmap (`/workflow/mindmap.mm.md`) is the conceptual overview of the project.
It is separate from the workbench — it does not track tasks, state, or progress.
It tracks *what the project is*: its central idea, its components, and how they relate.

The mindmap uses [Markmap](https://markmap.js.org/) syntax: a standard Markdown file
with a `markmap:` frontmatter block, rendered as an interactive visual map in VSCode
via the `gera2ld.markmap-vscode` extension. The file is plain Markdown; the visualization
is a consequence of opening it, not a separate artifact.

**When a project begins**, the mindmap contains only the central idea — a single top-level
heading. It grows as the project grows.

**Who updates it:**
The LLM proposes mindmap updates whenever a new conceptual feature is introduced — whether
by the user or the LLM — either mid-session or as part of the goodbye ritual. A proposal
takes the form: "Suggestion: add node X under Y, because Z." The user reviews and confirms
or revises before any change is written. The user may also edit the mindmap directly at
any time without going through the LLM.

**What the mindmap contains:**
Concepts, components, relationships, and open ideas. It is allowed to run ahead of the
code — a branch can exist in the mindmap before it is built. This makes it a useful space
for thinking, not just recording. Nodes not yet implemented are marked `[planned]`.

**What the mindmap does not contain:**
Tasks, status, dates, debt, or anything operational. Those live in the workbench and debt
tracker. The mindmap is purely conceptual.

**Structure conventions:**
- The root node is the project's central idea, as a top-level `#` heading.
- Major components or themes are `##` headings.
- Sub-concepts, relationships, and details are nested list items under those headings.
- Use `[planned]` to mark ideas not yet implemented.
- Use `[deprecated]` to mark concepts superseded but kept for context.

**Example structure for a new project:**

```markdown
---
markmap:
  colorFreezeLevel: 2
  initialExpandLevel: 2
---

# Project Name

## Core Idea
- What problem this solves
- Key insight or principle

## Components
- Component A [planned]
- Component B [planned]

## Open Questions
- How does X relate to Y?
```

The mindmap is a thinking tool, not a status board. It should feel like a map of the
project's intellectual territory, not a checklist.

---

## Part III — Pedagogical Layer

*Germane load is added deliberately here. This is how the user builds fluency over the
codebase, not just over individual components.*

---

### Cognitive Nudging and the Pseudocode Ladder

When intrinsic load is present in a component — meaning the user holds design intent,
behavioral logic, or domain knowledge that the LLM does not — pseudocode is expected
before implementation begins. When all remaining work is purely extraneous (formatting,
wiring, boilerplate with no design decisions), pseudocode is not required. If it is
unclear which applies, the LLM asks.

Pseudocode at any level of abstraction is valid. The LLM meets the user at whatever
rung of the ladder they choose.

**The Pseudocode Ladder:**

| Level | What it looks like |
|---|---|
| L0 | Natural language intent: "it should take a list and give back the top 3 by score" |
| L1 | Structured prose: "loop over items, keep a running top-3, return sorted" |
| L2 | Typed signatures and stubs: `def top_k(items: List[Item], k: int) -> List[Item]` |
| L3 | Near-code: partial logic with gaps, pseudocode syntax, rough control flow |

The LLM translates whatever level is given into working code, and asks clarifying questions
if the intent is ambiguous. It does not silently fill in intent that was not provided.
Only the general intent of the pseudocode is used as the source of truth —
the user specifies what, not how.

**Cognitive nudging:** At appropriate moments — when a new component is about to be
discussed, when a spec is still vague, when the user seems to be waiting for the LLM to
propose something — the LLM offers a nudge. Nudges are suggestive and non-prescriptive.
Example nudge:

> *"It might be useful to write a few lines of pseudocode here — even just natural language —
> to capture how you're imagining this working. That way we can build from your intent directly."*

Nudges do not prescribe what to write. They open a space. The user decides whether to fill it.

**The anti-crutch check:** If the user asks the LLM to write a spec, define behavior,
produce examples from scratch, or generate test cases — without any input — the LLM pauses
and nudges instead. The LLM never writes the spec. It never writes test logic. It translates,
formalizes, scaffolds, and challenges. When nudging toward tests, it asks questions that
help the user think of cases: "What should happen if the input is empty?" "What's the
largest input this needs to handle?" The user answers by writing the test.

---

### Desirable Difficulties

After each handshake closes, the LLM adds entries to the technique menu
(`/workflow/techniques.md`). This is a growing list of active learning prompts tied to
the work just completed, organized loosely by technique type. It is surfaced at session
close as part of the goodbye ritual.

**Technique types (to start):**

- **Retrieval practice:** "Without looking at the code, describe what `component_x` does."
- **Self-explanation:** "Walk me through why the tests for this component are structured the way they are."
- **Prediction:** "What will this function return given input Y?"
- **Generation effect:** A fill-in-the-blank version of a key function, for the user to complete.
- **Interleaving:** A question about an earlier component, prompted when it connects to the current one.

The technique menu is a living file. New techniques are added as they prove useful.
Techniques are scoped to the component just developed — not the whole codebase.
A spacing or review schedule for earlier components is not enforced automatically;
it can be requested by the user at any time.

**Delivery:** Difficulty prompts are surfaced at session close — never during active
development. They are lightweight, optional prompts the user can engage with between
sessions.

**Fluency measure:** For now, self-report and the quality of the user's pseudocode over
time serve as informal signals. A more rigorous measure will be designed as the workflow
matures.

---

## Part IV — Maintenance

*Keeping the system clean, organized, and honest about its own state.*

---

### Garbage Collection and Routine Reviews

The debt tracker (`/workflow/debt.md`) is a persistent record of everything that should be
improved but has not been yet. The LLM maintains it. The user reviews it.

**What goes in the debt tracker:**

- Dead code (unreachable, unused)
- Duplication (logic that exists in more than one place)
- Weak tests (tests that don't meaningfully constrain behavior)
- Missing or insufficient documentation
- Poor code quality (unclear naming, tangled logic, lack of structure)

**Debt tracker entry format:**

```
[date identified] | [type] | [location] | [description] | [proposed fix] | [status: open/in-progress/resolved]
```

**Review cadence:** The LLM runs a GC pass at session end, as step 5 of the goodbye ritual.
It scans the debt tracker, reviews shared code for new issues, and proposes updates.
The user reviews and sets priorities at the start of the next session if needed.

**GC pass — step by step:**

1. Read the debt tracker; flag items marked open that touch the current focus area.
2. Ask the user for the codebase context to scan — typically the current git repository
   or a relevant subset of it. The user shares what is appropriate.
3. Review the shared code for new instances of the debt categories above.
4. Check that tests still match the current spec (drift detection).
5. Propose any new debt entries with descriptions and proposed fixes.
6. Update debt tracker statuses for anything resolved since last session.
7. Summarize: "X open items, Y new items found, Z resolved."

The GC pass is a proposal, not an interruption. The user decides what to act on.

---

### Archiving and Organization

Archiving is a separate process from garbage collection. It is triggered by the user,
not by a schedule.

**When the user asks to archive something**, the LLM:

1. Moves the relevant files to `/archive/` with a subdirectory named by component and date.
2. Adds an entry to the log recording what was archived and why.
3. Updates the workbench to remove the item from active lists.
4. Asks the user: delete the original, keep it in git history only, or keep both?
   The user decides. The LLM does not delete anything without explicit instruction.

**Naming convention for archives:**
```
/archive/<component_name>_<YYYY-MM-DD>/
```

**Organization convention for active files:** Files follow the directory layout defined
in Foundations. The LLM flags any file that does not conform during the GC pass.

---

## A Note on This Document

This guide is a living document. When a section proves wrong, incomplete, or cumbersome in
practice, the user and LLM update it together — using the same workflow it describes.
The guide is not handed down; it is grown.

Current open items:
- Desirable Difficulties: Fluency measure — to be designed as the workflow matures.
- Meta: Worked example — one component end-to-end, to pressure-test the whole guide.
