# Running `build.py`

`build.py` is the executable form of [build.md](build.md)'s transform,
hardcoded to this repo's `Blueprint/ -> Agent/`. This file tells an
agent how to actually *run* it. It is not part of the `>`/`>>`/`>>>`
command surface `Blueprint/README.md` describes — regenerating `Agent/`
is a separate, one-off meta-process, same as `build.md` says.

## Why you can't just `python build.py`

`Builder.do()` is a stub — it `pass`es, returning `None`. Every
judgment step in `build.py` (reading and understanding `Blueprint/`,
designing a command tree, writing actual README/package content)
routes through `do(task)`. Run the file with a plain interpreter and
the procedural skeleton executes fine, but every `do(...)` call
contributes nothing, and downstream writes end up empty. That's by
design — see `build.md` Step 4: `do()` is filled in by whoever is
*executing* the pseudocode, not by the interpreter.

## How to actually execute it

Work through `Builder.run()` yourself, method by method, in the order
it calls them (`verify_env` -> `read_everything` ->
`design_command_structure` -> `build_package` -> `verify_checklist`).
Within each method, go line by line, using only that line's local
state — the same discipline `build.md`-generated agents follow when
executing their own pseudocode. Every line must be followed strictly,
in the order it appears — none skipped, reordered, or batched from
memory, even when a later line looks predictable from an earlier one.

- **Procedural lines** (existence checks, `mkdir`, listing files under
  `Blueprint/`) — these are real, correct Python. If a line isn't a
  `self.do(task)` call, actually execute it with real Python (you have
  shell/file tools) rather than only approximating the equivalent
  action by hand — the interpreter gets these right for free, so there's
  no reason to simulate them.
- **`self.do(task)` lines** — stop, read `task`, and personally carry
  it out using your own reasoning and tools (reading files under
  `Blueprint/`, thinking through design decisions, drafting content).
  Treat whatever you produce as that call's return value and carry it
  forward into the next line exactly as written (e.g. `notes = ...`
  means the next steps' `notes!r}` should reflect what you actually
  produced, not the literal string).
- **Where a `do()` result feeds a `.write_text(...)` call** — actually
  write that file for real, with your file-editing tools, using the
  content you produced. Don't leave it as a no-op just because the
  underlying Python would; per `build.md`'s Objective, carry out each
  step's real underlying action wherever you have the tools to.

## Order matters

Don't skip ahead or batch steps from memory. `read_everything`'s notes
feed `design_command_structure`; both feed every write in
`build_package`. If you improvise content without actually having read
`Blueprint/` first, you've broken the same rule `build.md` Step 1
states directly: read everything before writing any code.

## When you're done

Re-check `verify_checklist`'s `do(...)` task against what actually
exists on disk — `Agent/`, `./README.md`, `./CLAUDE.md` — not against
what you intended to produce. If something's missing or stale, go back
and fix it; don't report success from a plan.

## After reading this file

Don't start executing `Builder.run()` on your own initiative. This is a
one-off, repo-wide regeneration of `Agent/` — ask the user whether they
want to proceed with the transformation before doing anything else,
and wait for their answer.

