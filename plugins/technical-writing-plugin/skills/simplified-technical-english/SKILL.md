---
name: simplified-technical-english
description: Rewrites technical documentation into ASD-STE100 style — one meaning per word, active voice, simple tenses, short sentences, no ellipsis. Use when writing or editing READMEs, ADRs, specs, runbooks, API docs, release notes, error messages, commit messages, or agent-facing text, and when asked to "simplify this", "tighten this doc", or "STE rewrite".
---

# Simplified Technical English (ASD-STE100)

ASD-STE100 is a controlled-language standard built by the AeroSpace and Defence Industries Association of Europe. Its purpose is to stop maintenance technicians from misreading English instructions, often when English is not their first language. The standard attacks the two largest sources of misreading: words that carry more than one meaning, and sentences that permit more than one structure.

This skill applies that discipline to technical documentation generally. The reader may be an on-call engineer reading a runbook at 03:00, a reviewer skimming an ADR, a non-native English speaker following a setup guide, a translation pipeline, or an AI agent parsing a tool description. None of them can ask a follow-up question. If a technician can read "close the valve" as a description of a nearby valve instead of a command, so can every reader above.

The goal is text with exactly one possible reading.

## When to Use This Skill

Use it when writing or editing:

| Document type | Why STE helps |
| ------------- | ------------- |
| Runbooks, incident procedures | The reader is under time pressure and must not re-parse a sentence |
| Setup guides, READMEs | Readers span skill levels and first languages |
| ADRs, specs, design docs | Ambiguous scope wording becomes an ambiguous decision |
| API reference, error messages | Short strings carry no context to disambiguate them |
| Commit messages, PR descriptions | Read out of context, months later, by someone else |
| Agent-facing text — prompts, tool descriptions, inter-agent instructions | No human is present to resolve ambiguity |
| Anything heading into translation | Ambiguity multiplies across languages |

Also use it as a review pass: run it over an existing document and report which rules the document breaks, without rewriting anything, when the user asks for a check rather than an edit.

Do not use it for creative, marketing, or persuasive copy. STE is deliberately flat and literal. Voice and nuance are losses there, not gains.

## Source and Scope

This skill encodes the **rule categories** of ASD-STE100: writing rules organised into nine sections covering word choice, noun phrases, verbs, sentences, procedural and descriptive writing, safety instructions, punctuation, and general writing practice. The standard is backed by a dictionary of roughly 900 approved words, each with one meaning and one part of speech, plus a larger list of words to avoid with approved replacements. `references/writing-rules.md` summarises the nine sections.

This skill does **not** reproduce ASD's dictionary. The official standard is a free download from ASD and remains the source of truth for exact approved wording and exact rule numbering. Instead, this skill applies the underlying principle: pick the plainest, most common word available, and use it the same way every time.

When exact ASD-approved wording matters — real aircraft or defence maintenance documentation — download the standard from <https://www.asd-ste100.org/> and check word by word against the real dictionary. Do not rely on this skill for that purpose.

## Core Rewrite Rules

| Rule | Do | Do not |
| ---- | -- | ------ |
| One word, one meaning | Choose one verb per action and reuse it. Always "check", never "check" then "verify" then "confirm" for the same action | Rotate synonyms for the same idea across a document |
| One part of speech per word | "Apply oil to the bearing" — *oil* is a noun | "Oil the bearing" — *oil* becomes a verb |
| Active voice | "The scheduler deletes the job." | "The job is deleted." — unless the actor is genuinely unknown |
| Simple tenses only | "We received the report." | "We have received the report." |
| One instruction per sentence | "Open the file. Read line 3." | "Open the file and read line 3, then check whether it matches." |
| Sentence length | 20 words or fewer for instructions; 25 or fewer for descriptions | Long chains of subordinate clauses |
| Noun clusters | Three words maximum. "fuel pump valve" | "high pressure fuel pump inlet valve assembly" |
| No ellipsis | Keep the subject, verb, and article explicit, even when it reads longer | "Files not backed up will be lost" — which files? |
| Paragraphs | One topic per paragraph, six sentences maximum | Paragraphs that change subject halfway |
| Lists for sequences | Use a numbered list for three or more ordered steps | Bury a sequence inside one prose sentence |
| Conditions before instructions | "If the check fails, restart the service." | "Restart the service if the check fails." — the reader may act before reading the condition |
| Warnings before the step | Put the warning immediately before the step it applies to | Collect warnings at the end of a procedure |
| Domain terms | Keep necessary technical nouns and verbs. Define each one once. STE permits a project glossary beyond its base dictionary | Use jargon that the document never defines |

### Applying the rules by document type

**Procedures and runbooks.** Enforce the 20-word limit strictly. One instruction per numbered step. State the condition first, then the action. Put each warning directly above its step. Name the actor even when it seems obvious.

**Descriptive text — READMEs, ADRs, design docs.** Allow 25 words per sentence and six sentences per paragraph. Active voice still applies. Passive voice is acceptable only where the actor is genuinely unknown or irrelevant, and this exception is rare in a design document.

**Short strings — errors, log lines, tool descriptions.** These have no surrounding context, so ambiguity is unrecoverable. State what happened, what caused it, and what the reader should do. Do not compress by dropping articles: "Config file not found" is weaker than "The server did not find the config file at /etc/app.yaml."

## Process

1. Read the input once for meaning. Do not rewrite before you understand what the text must still say afterwards.
2. Identify the document type and the reader. This sets the sentence limit and decides how much domain vocabulary must survive.
3. Walk the text sentence by sentence. Flag every violation: ambiguous word, compound tense, passive voice, over-length sentence, ellipsis, noun stack, buried condition.
4. Rewrite each flagged sentence to remove the violation while preserving the meaning exactly.
5. Where a rewrite would drop necessary precision — a safety condition, a scope qualifier, a number, a named exception — keep the longer phrasing and flag the trade-off. Precision outranks brevity every time.
6. Produce the before and after table below.
7. If the text already complies, say so. Do not force changes onto compliant text.

## Output Format

```markdown
| Rule violated | Original | Simplified |
|---|---|---|
| Present perfect tense | "We have received your request." | "We received your request." |
| Noun cluster (4+ words) | "the agent task queue priority handler" | "the handler that sets task-queue priority" |
| Buried condition | "Restart the service if the check fails." | "If the check fails, restart the service." |
| Ellipsis | "Files not backed up will be lost." | "The installer deletes any file that it did not back up." |
```

Follow the table with a short note listing anything you deliberately left unsimplified, and why. The usual reason is that simplifying would lose required precision.

When the user asked for a review rather than an edit, produce the same table with the Simplified column filled in as a suggestion, and do not modify the file.

## Boundaries

**Will:**

- Rewrite dense or ambiguous technical English into short, single-meaning, active-voice sentences.
- Name the specific rule a sentence breaks before rewriting it.
- Preserve every fact, condition, number, and scope qualifier in the original.
- Suggest a one-line glossary entry for each domain term that must stay.
- Adjust sentence and paragraph limits to the document type.

**Will not:**

- Reproduce ASD's approved dictionary from memory as if it were authoritative. The official download is the source of truth for exact wording.
- Simplify creative, marketing, or persuasive copy.
- Drop a safety condition, exception, or qualifier to shorten a sentence. It flags the trade-off instead.
- Strip domain vocabulary that the reader needs. A term is replaced only when a plainer word means exactly the same thing.
- Claim STE compliance. This is a general-purpose clarity tool modelled on STE, not a certified STE authoring tool.

## Additional Resources

- `references/writing-rules.md` — the nine rule sections in more detail, with notes on the dictionary and on citing the standard.
- `examples/before-after.md` — worked examples across runbooks, ADRs, error messages, and tool descriptions.
