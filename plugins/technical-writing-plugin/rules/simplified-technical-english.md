# Simplified Technical English

Apply these rules when you write documentation, commit messages, PR descriptions, error messages, log lines, or agent-facing text. Do not apply them to chat replies or to creative and marketing copy.

- One word, one meaning. Pick one verb per action and reuse it. Do not rotate synonyms.
- Use active voice. Use passive voice only when the actor is unknown.
- Use simple tenses. "We received", not "we have received".
- Write one instruction per sentence. Instructions: 20 words or fewer. Descriptions: 25 words or fewer.
- Use three-word noun clusters at most.
- Do not drop subjects, verbs, or articles. "The server did not find the config file at /etc/app.yaml", not "Config file not found".
- Put the condition before the instruction: "If the check fails, restart the service."
- Put a warning immediately before the step it applies to.
- Use a numbered list for three or more ordered steps.
- Define each domain term once. Keep it if the reader needs it.
- Precision outranks brevity. Never drop a condition, number, or exception to shorten a sentence.

For a full rewrite or review, use `/ste` or `/ste-review`.
