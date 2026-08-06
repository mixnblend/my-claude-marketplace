---
description: Rewrite technical documentation into Simplified Technical English (ASD-STE100 style)
---

# Simplify Technical English: $ARGUMENTS

## Objective

Rewrite the target text into Simplified Technical English: one meaning per word, active voice, simple tenses, short sentences, no ellipsis. Preserve every fact, condition, number, and scope qualifier.

## Prerequisites

Load the `simplified-technical-english` skill before you start. Read its reference files if the text is a procedure or contains safety conditions:

- `${CLAUDE_PLUGIN_ROOT}/skills/simplified-technical-english/references/writing-rules.md`
- `${CLAUDE_PLUGIN_ROOT}/skills/simplified-technical-english/examples/before-after.md`

## Target

`$ARGUMENTS` names the file, section, or pasted text to rewrite. If it is empty, ask which text to rewrite before you continue.

## Process

Follow the skill's process. Identify the document type first, because it sets the sentence limit. Apply the edits to the file, then output the before and after table so the user can review each change.

Close with a note listing anything you left unsimplified and why.
