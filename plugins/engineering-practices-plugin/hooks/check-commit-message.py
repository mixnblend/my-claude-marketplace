#!/usr/bin/env python3
"""PreToolUse hook: block a `git commit` whose subject is not a conventional commit.

Reads the hook input from stdin. Exits 2 with a reason on stderr to block the
commit. Exits 0 when the command is not a commit, or when the message cannot be
read from the command (an editor commit, `--no-edit`, or an unusual quoting).
"""

import json
import os
import re
import sys

TYPES = ("feat", "fix", "refactor", "chore", "docs", "ci")
SUBJECT = re.compile(r"^(%s)(\([a-z0-9._/-]+\))?!?: \S" % "|".join(TYPES))
SKIP_PREFIXES = ("Merge ", "Revert ", "fixup! ", "squash! ", "amend! ")

GIT_COMMIT = re.compile(r"\bgit\s+(?:-C\s+\S+\s+)?commit\b")
HEREDOC = re.compile(r"<<-?\s*['\"]?(\w+)['\"]?\n(.*?)\n\s*\1\b", re.S)
MESSAGE_FLAG = re.compile(
    r"(?:\s-[a-zA-Z]*m|\s--message)[= ]?\s*(?:\"((?:[^\"\\]|\\.)*)\"|'([^']*)')"
)
FILE_FLAG = re.compile(r"(?:\s-F|\s--file)[= ]?\s*(\S+)")


def first_line(text):
    for line in text.splitlines():
        if line.strip():
            return line.strip()
    return None


def read_subject(command, cwd):
    heredoc = HEREDOC.search(command)
    if heredoc:
        return first_line(heredoc.group(2))

    message = MESSAGE_FLAG.search(command)
    if message:
        return first_line(message.group(1) or message.group(2) or "")

    message_file = FILE_FLAG.search(command)
    if message_file:
        path = os.path.join(cwd, message_file.group(1).strip("'\""))
        try:
            with open(path) as f:
                return first_line(f.read())
        except OSError:
            return None

    return None


def main():
    hook_input = json.load(sys.stdin)
    command = hook_input.get("tool_input", {}).get("command", "")
    if not GIT_COMMIT.search(command):
        return 0

    subject = read_subject(command, hook_input.get("cwd", os.getcwd()))
    if not subject or subject.startswith(SKIP_PREFIXES):
        return 0
    if SUBJECT.match(subject):
        return 0

    print(
        f'The commit subject "{subject}" does not follow the conventional commit format.\n'
        "Use `type(scope): description` in the imperative mood.\n"
        f"Allowed types: {', '.join(TYPES)}. There is no `test` type: use `chore` for test-only changes.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
