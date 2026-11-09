#!/usr/bin/env bash
# PostToolUse hook: run markdownlint-cli2 on a Markdown file under docs/ that
# Claude just wrote or edited. Exits 2 so that Claude sees the problems. Does
# not change the file. Skips silently when markdownlint-cli2 is not installed.

file=$(jq -r '.tool_input.file_path // empty')
project_dir="${CLAUDE_PROJECT_DIR:-$(pwd)}"

[[ "$file" == *.md && -f "$file" ]] || exit 0
[[ "$file" == "$project_dir"/docs/* || "$file" == docs/* ]] || exit 0
command -v markdownlint-cli2 >/dev/null || exit 0

if ! output=$(cd "$project_dir" && markdownlint-cli2 "$file" 2>&1); then
  printf 'markdownlint-cli2 found problems in %s. Run: markdownlint-cli2 --fix "%s"\n%s\n' \
    "$file" "$file" "$output" >&2
  exit 2
fi
