---
description: Review technical documentation against ASD-STE100 rules without editing it
---

# Review Technical English: $ARGUMENTS

## Objective

Review the target text against the Simplified Technical English rules and report what it breaks. Do not edit any file.

## Prerequisites

Load the `simplified-technical-english` skill before you start.

## Target

`$ARGUMENTS` names the file or directory to review. If it is empty, review the documents changed on the current branch.

## Process

Walk the text sentence by sentence. Flag every violation: ambiguous word, inconsistent synonym, compound tense, passive voice, over-length sentence, ellipsis, noun cluster of four or more words, buried condition, misplaced warning, undefined jargon.

Output the before and after table from the skill, with the Simplified column filled in as a suggestion rather than an applied edit. Order the rows worst first: safety and ambiguity problems before style problems.

If the text complies, say so and stop. Do not manufacture findings.
