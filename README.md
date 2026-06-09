# TDD with LLM Agents

A project template for collaborative, test-driven development with an LLM agent. Built around one idea: **you should understand everything you build.** The LLM handles the mechanical work; you own the thinking.

---

## The Problem This Solves

Most people use LLMs for coding the same way: describe what you want, get code back, move on. It works — until you need to debug it, extend it, or explain it to someone else. You got the output without building the understanding.

This template structures the collaboration differently. The LLM writes code; you write the spec that tells it what to write. The LLM runs the paperwork; you make every meaningful decision. The distinction is deliberate and enforced throughout.

The underlying framework comes from cognitive load theory. There are three kinds of cognitive load: *intrinsic* (the genuine difficulty of understanding the problem), *extraneous* (incidental friction like syntax and formatting), and *germane* (the effort that actually builds lasting knowledge). The goal is to offload extraneous load to the LLM, keep intrinsic load with you, and deliberately add germane load so you grow fluent over what you build.

---

## What's in This Template

```
/src                     — your source code
/tests                   — your test files
/workflow                — all project meta-files (see below)
/workflow/reports        — one report per completed feature
/archive                 — settled or superseded work
run_tests.py             — test runner
pytest.ini               — pytest configuration
WORKFLOW_GUIDE.md        — the full guide for you and the LLM
README.md                — this file
```

The `/workflow` folder is the persistent brain of the project:

| File | What it is |
|---|---|
| `workbench.md` | Current project state: focus, pending work, open decisions |
| `log.md` | Append-only record of everything that happened |
| `debt.md` | Technical debt tracker |
| `techniques.md` | Active learning prompts generated after each feature |
| `mindmap.mm.md` | Conceptual map of the project, rendered with Markmap |

All of these are committed to version control. They are not scratch notes — they are the project record.

---

## How It Works

Development happens in **handshakes**: units of collaborative work that always follow the same shape.

```
Proposal → Conversation → Spec (you write) → Tests → Implementation → Report → Review
```

A handshake can be proposed by either you or the LLM. It ends when you explicitly close it. The spec always comes before the tests. The tests always come before the code. No exceptions.

**Every session starts with a hello ritual** — the LLM reads the workbench and log, summarizes where things stand, and you confirm or correct before any work begins. You never have to re-explain the project from scratch.

**Every session ends with a goodbye ritual** — triggered by saying *"Ok, Goodbye!"* The LLM updates all the meta-files, proposes any changes to the mindmap, runs a garbage collection pass on the codebase, and surfaces a few active learning prompts for you to think about between sessions.

---

## Your Role vs. the LLM's Role

This is the most important part of the template. It is worth reading carefully.

**You always own:**
- Writing what a component should do, in plain language
- Providing examples and edge cases — even rough ones
- Writing pseudocode when you have a design in mind
- Writing all test logic — the assertions, the cases, and the intent behind each one
- Making decisions when there are real tradeoffs
- Understanding *why* the code works, not just that it does
- Signing off on specs before tests are written

**The LLM always owns:**
- Translating your spec and pseudocode into working code
- Writing test file boilerplate and framework wiring — never the test logic itself
- Formatting, linting, and file conventions
- Maintaining the workbench, log, reports, debt tracker, and mindmap

**The LLM never generates test cases on its own.** If you ask it to, it will ask you
questions instead — "what should happen if X is empty?", "what's the failure case here?"
— and wait for you to write the test. It will actively push you to think of more cases,
using a coverage heuristic as a prompt. The test suite is yours.

---

## Pseudocode Is a First-Class Input

You don't need to write perfect code to drive this workflow. You can write at any level of abstraction and the LLM will meet you there:

| Level | Example |
|---|---|
| Plain language | *"it should take a list and return the top 3 items by score"* |
| Structured prose | *"loop over items, keep a running top-3, return sorted"* |
| Typed stubs | `def top_k(items: List[Item], k: int) -> List[Item]` |
| Near-code | Partial logic with gaps, rough control flow |

The LLM translates your intent into working code. It will ask clarifying questions if something is ambiguous. It will never silently fill in intent you didn't provide.

When a good moment to write pseudocode arrives, the LLM will suggest it — not prescribe it. You decide whether to take it up.

---

## The Mindmap

The project mindmap (`/workflow/mindmap.mm.md`) is a [Markmap](https://markmap.js.org/) file — plain Markdown that renders as an interactive visual map in VSCode via the [Markmap extension](https://marketplace.visualstudio.com/items?itemName=gera2ld.markmap-vscode).

It is the conceptual overview of the project: what it is, how the parts relate, and what is still open. It is not a task list or a status board — those live in the workbench. The mindmap is allowed to run ahead of the code. If you have an idea that isn't built yet, it belongs in the mindmap marked `[planned]`.

The LLM proposes mindmap updates whenever a new conceptual feature is introduced. You confirm before anything is written.

---

## Getting Started

**1. Clone or fork this template.**

**2. Install dependencies.**

```bash
pip install pytest
```

**3. Seed the project.**

Open `/workflow/workbench.md` and fill in:
- Project Conventions (any naming or style conventions beyond the defaults)

Open `/workflow/mindmap.mm.md` and replace "Project Name" with your project's name and seed the Core Idea section with a sentence or two about what you're building.

**4. Verify the test runner works.**

```bash
python run_tests.py
```

You should see one passing test (`test_placeholder.py`). Delete that file once your first real component has its own tests.

**5. Start your first session.**

Paste the contents of `WORKFLOW_GUIDE.md` into your LLM's context, or attach it as a file. Tell the LLM: *"This is our workflow guide. Let's start the first session."*

The LLM will run the initialization ritual: confirm the starter files, ask you to fill in any missing conventions, and ask what you want to build first.

---

## Running Tests

```bash
python run_tests.py                          # Run all tests
python run_tests.py --component <name>       # Run tests for one component
python run_tests.py --verbose                # Verbose output
```

The `--component` flag resolves `<name>` to `tests/test_<name>.py`. If the file doesn't exist, the runner tells you clearly.

---

## Adapting This Template

This template is Python and pytest by default. To adapt it:

- Change the test runner to call your framework of choice
- Update `pytest.ini` or replace it with the equivalent config
- Update the conventions in `workbench.md`
- Tell the LLM at the start of the first session

The workflow itself — handshakes, specs, rituals, mindmap, debt tracker — is framework-agnostic. Only the test runner is language-specific.

---

## Philosophy

This template is opinionated about one thing: **LLMs should make you better at your work, not remove you from it.**

The mechanical parts of software development — syntax, boilerplate, formatting, bookkeeping — are real friction, and it makes sense to hand them off. But the parts that require judgment, design thinking, and genuine understanding of the problem are where fluency lives. Handing those off too produces code you can't maintain, can't extend, and can't explain.

The structure here is designed so that the LLM is genuinely useful without quietly doing the thinking for you. The rituals, the pseudocode ladder, the handshake protocol, the desirable difficulty prompts at the end of each session — all of it exists to keep the intrinsic load where it belongs.

---

## License

MIT
