# Build

`Build` turns a directory of documentation into an installable Python package meant to be *executed by an AI agent's own reasoning*, not run as ordinary code.

## Files

- [`build.md`](build.md) — tells an agent how to actually carry out `build.py`'s process by hand: which lines are real, runnable Python (execute them for real) and which are `self.do(task)` judgment calls (carry out using your own reasoning, feeding the result forward into later steps exactly as written).
- [`build.py`](build.py) — the executable skeleton of that process: a `Builder` class whose `run()` method calls, in order, `verify_env -> read_everything -> design_command_structure -> build_package -> verify_checklist`. Every step requiring judgment routes through `self.do(task)`, which is a stub under a plain interpreter — see `build.md` for why, and how to actually execute it.

## Usage

Point an AI agent at this pair of files and ask it to read `build.md`, then work through `build.py`'s `Builder.run()` by hand, in order, following `build.md`'s instructions.

By default, `Builder` reads source docs from `./Blueprint` and writes the generated package to `./Agent`, both resolved relative to wherever `build.py` is invoked from. Override either with `--input`/`--output`:

```bash
python build.py --input <docs-dir> --output <package-dir>
```

Running it with a plain interpreter only executes the procedural scaffolding (directory checks, `mkdir`s) — every judgment step (reading the docs, designing a command tree, writing file content) needs an agent to actually carry it out; see `build.md`.

## What gets produced

Whatever `<output-dir>` ends up containing (default `Agent/`):

- an installable `agent` Python package, with one small method per capability described in the source docs, and `Agent.do(self, task: str)` as the fallback for anything that isn't cleanly proceduralizable
- `<output-dir>/README.md`, documenting the generated package's install and usage
- the repository root's `README.md` and `CLAUDE.md`, updated to point at the generated package

This is a one-off, repo-wide regeneration — `build.md` tells the agent not to start it unprompted, and to ask for confirmation first.
