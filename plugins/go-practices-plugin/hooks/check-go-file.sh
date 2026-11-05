#!/usr/bin/env bash
# PostToolUse hook: report gofmt and go vet problems in a Go file that Claude
# just wrote or edited. Exits 2 so that Claude sees the report. Does not change
# the file.

file=$(jq -r '.tool_input.file_path // empty')

[[ "$file" == *.go && -f "$file" ]] || exit 0
command -v go >/dev/null || exit 0

problems=""

unformatted=$(gofmt -l "$file" 2>&1)
if [[ -n "$unformatted" ]]; then
  problems+="gofmt: $file is not formatted. Run: gofmt -w $file"$'\n'
fi

vet_output=$(cd "$(dirname "$file")" && go vet . 2>&1)
if [[ $? -ne 0 ]]; then
  problems+="go vet failed in $(dirname "$file"):"$'\n'"$vet_output"$'\n'
fi

if [[ -n "$problems" ]]; then
  printf '%s' "$problems" >&2
  exit 2
fi
