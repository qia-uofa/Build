"""
Executable form of build.md's Documentation -> Python Package
Transformer, defaulting to this repository's own run of it:
INPUT=Blueprint, OUTPUT=Agent, overridable via --input/--output.
(build.md itself stays generic/parameterized; this is one concrete run
of it, composed the same way build.md instructs any $INPUT to be
composed into Python: procedural steps as real, runnable code, judgment
steps routed through do().)

Like the packages this process generates, an ordinary Python runtime
is not the intended reader. Procedural steps (file existence checks,
directory scaffolding, listing files) are real and may be run for
real. Every step requiring judgment (reading and understanding
Blueprint/, designing a command tree, writing actual file content)
routes through do() and must be carried out by the executing agent's
own reasoning, not by this interpreter -- see run_build.md.
"""

import argparse
from pathlib import Path

DEFAULT_INPUT = Path("Blueprint")
DEFAULT_OUTPUT = Path("Agent")


class Builder:
    def __init__(self, input_dir: Path = DEFAULT_INPUT, output_dir: Path = DEFAULT_OUTPUT):
        self.input = input_dir
        self.output = output_dir

    def do(self, task: str):
        """
        Escape hatch for judgment calls this script can't express as
        deterministic code. `task` is what to do; the return value is
        whatever the caller needs (str, list, dict, ...). Carried out
        by the executing agent's own reasoning, not this interpreter.
        """
        pass

    def run(self):
        self.verify_env()
        notes = self.read_everything()
        command_tree = self.design_command_structure(notes)
        self.build_package(notes, command_tree)
        self.verify_checklist()

    def verify_env(self):
        assert self.input.is_dir(), f"{self.input} must exist and contain the source docs"
        self.output.mkdir(exist_ok=True)
        if any(self.output.iterdir()):
            self.do(
                f"An existing package was found at {self.output}. Read it, "
                f"diff it against the current contents of {self.input}, and "
                "treat it as a starting point: fill in what's missing, "
                "update what's stale, restructure whatever no longer "
                "matches the command tree or module layout Blueprint/ "
                "implies. Don't regenerate from scratch."
            )

    def read_everything(self):
        source_files = sorted(p.relative_to(self.input) for p in self.input.rglob("*") if p.is_file())
        return self.do(
            f"Read every file under {self.input}/ before writing any code: "
            f"{source_files}. While reading, identify: the domain/purpose "
            "of the agent; every distinct action or capability described; "
            "any command hierarchy or CLI syntax already specified; "
            "implicit groupings of actions that suggest a command tree "
            "(verbs, nouns, subcommands); state the agent needs to carry "
            "between actions; steps described only in prose with no clean "
            "procedural translation. Return your notes."
        )

    def design_command_structure(self, notes):
        return self.do(
            f"Given these notes on {self.input}/: {notes!r} -- design a "
            "(possibly nested) command-line structure. Use an explicit "
            "command tree/CLI syntax from the docs as-is if one exists; "
            "otherwise infer a reasonable tree the way a well-designed CLI "
            "groups related actions under shared verbs/nouns (think `git "
            "remote add`, `docker container ls`). Do not mirror the source "
            "docs' own structure (section headings, chapter order) -- "
            "build it the way an idiomatic Python package would be built. "
            "Return the command tree."
        )

    def build_package(self, notes, command_tree):
        self._scaffold_layout()
        self._write_output_readme(notes, command_tree)
        self._write_root_docs(notes)
        self._write_agent_package(notes, command_tree)

    def _scaffold_layout(self):
        (self.output / "agent").mkdir(exist_ok=True)
        (self.output / "agent" / "commands").mkdir(exist_ok=True)

    def _write_output_readme(self, notes, command_tree):
        content = self.do(
            f"Write {self.output}/README.md as a standard GitHub-style "
            "README (what it does, install, usage, command reference) "
            "that introduces the Agent class as the main entry point. If "
            f"{self.input}/ specifies a runtime execution/UX contract for "
            "the generated agent (how it interprets user input, when it "
            "must confirm before acting, an execution model, a required "
            "logging/tracing format), transcribe it completely and "
            "exactly as documented -- don't weaken, simplify, reorder, or "
            "invent one if unspecified. "
            f"Notes: {notes!r}. Command tree: {command_tree!r}."
        )
        (self.output / "README.md").write_text(content or "", encoding="utf-8")

    def _write_root_docs(self, notes):
        readme = self.do(
            "Write or update ./README.md at the repository root: the "
            f"project-level readme introducing the two-layer system "
            f"({self.input}/ as source spec, {self.output}/ as generated "
            "package), the repository layout, how the pieces relate, and "
            f"pointing to {self.output}/README.md as the canonical "
            "operating manual. Treat any existing ./README.md as a "
            "starting point to update in place, not a template to "
            "overwrite blindly."
        )
        Path("README.md").write_text(readme or "", encoding="utf-8")
        self._append_build_usage()

        claude_md = self.do(
            "Write or update ./CLAUDE.md at the repository root: a short "
            f"pointer telling Claude Code to read {self.output}/README.md "
            f"before acting on anything in the project, and naming "
            f"{self.input}/ as the read-only source spec the package was "
            "generated from (referencing Build/build.md for the "
            "transformation rules). Treat any existing ./CLAUDE.md as a "
            "starting point."
        )
        Path("CLAUDE.md").write_text(claude_md or "", encoding="utf-8")

    def _append_build_usage(self):
        marker = "The following is appended by the execution of build.py"
        usage = self.do(
            "Write a 'Usage of Build/build.md' section documenting how to "
            "actually run Build/build.md's regeneration process: that "
            "Build/build.md tells an agent how to manually execute "
            "Build/build.py's Builder.run() (verify_env -> "
            "read_everything -> design_command_structure -> "
            "build_package -> verify_checklist) since Builder.do() is a "
            "stub returning None under a plain interpreter; the "
            "distinction between procedural lines (run for real) and "
            "self.do(task) lines (carried out by the executing agent's "
            "own reasoning, feeding forward into later steps exactly as "
            "written); that steps must not be skipped or batched from "
            "memory since notes flow downstream; that verify_checklist "
            "must be re-checked against what actually exists on disk, not "
            "what was intended; that this is a one-off meta-process never "
            "started on the agent's own initiative; and the "
            "--input/--output flags Build/build.py accepts. Do not "
            "include this marker line itself in your output -- it is "
            "prepended separately."
        )
        with open("README.md", "a", encoding="utf-8") as f:
            f.write(f"\n\n---\n\n{marker}\n\n{usage or ''}\n")

    def _write_agent_package(self, notes, command_tree):
        self.do(
            f"Generate {self.output}/agent/** and {self.output}/"
            "pyproject.toml: Agent as the central class; one small, "
            "single-purpose method per CLI command, split across "
            "submodules mirroring the CLI's nesting when the tree is deep "
            "(not the source docs' nesting); a CLI entry point wiring "
            "parsed args to methods (pseudocode, never needs to actually "
            "run); do(self, task: str) on the base/Agent class as the "
            "fallback for steps with no clean procedural translation, "
            "including error-handling branches that can't be judged "
            "deterministically. Apply modularity rules: one responsibility "
            "per method; shared logic extracted into utilities; related "
            "commands grouped into their own modules/classes composed by "
            "Agent; clear names over comments. "
            f"Notes: {notes!r}. Command tree: {command_tree!r}."
        )

    def verify_checklist(self):
        self.do(
            "Verify against build.md's Step 6 checklist: package named "
            f"exactly `agent`, rooted at {self.output}/; "
            f"{self.output}/README.md exists, documents install/usage, "
            "and introduces the Agent class; ./README.md and ./CLAUDE.md "
            f"exist at the repository root and correctly reference "
            f"{self.input}/{self.output}; every capability in "
            f"{self.input}/ maps to a concrete method or a do(...) call; "
            "the CLI command tree reflects the docs' explicit structure "
            "or a reasonable inferred one; do() exists and is used "
            "consistently, not as a dumping ground; no dead scaffolding, "
            "no comments explaining *what* the code does; the layout "
            "reads like an ordinary, idiomatic installable Python "
            "package."
        )


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-i", "--input", type=Path, default=DEFAULT_INPUT,
        help=f"directory of source docs to transform (default: {DEFAULT_INPUT})",
    )
    parser.add_argument(
        "-o", "--output", type=Path, default=DEFAULT_OUTPUT,
        help=f"directory the generated `agent` package is written to (default: {DEFAULT_OUTPUT})",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    Builder(args.input, args.output).run()
