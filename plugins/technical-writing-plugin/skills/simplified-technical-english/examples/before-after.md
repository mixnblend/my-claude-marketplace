# Worked Examples

Each example shows the rule broken, the original text, and the rewrite. These are illustrative examples written for this skill, not extracts from the standard.

## Runbook step

Original:

> If the health endpoint has been returning 503s for more than five minutes and the pod restart count has been incrementing, the service should be drained from the load balancer and restarted, after which the on-call engineer needs to be notified.

| Rule violated | Fix |
| ------------- | --- |
| Sentence length (48 words, limit 20) | Split into four steps |
| Present perfect continuous | Simple present |
| Passive voice, actor removed | Name the actor |
| Multiple instructions in one sentence | One instruction per step |

Rewrite:

> 1. Check the health endpoint. If it returns 503 for more than five minutes, continue to step 2.
> 2. Check the pod restart count. If the count increases, continue to step 3.
> 3. Drain the service from the load balancer.
> 4. Restart the service.
> 5. Notify the on-call engineer.

## ADR sentence

Original:

> We have decided to go with the event-driven approach, which was chosen mainly due to the fact that the alternative would have introduced tight coupling between services, though there are some latency implications.

| Rule violated | Fix |
| ------------- | --- |
| Present perfect | Simple past |
| Wordy phrase (*due to the fact that*) | *because* |
| Two topics in one sentence | Split |
| Vague qualifier (*some latency implications*) | State the number, or flag that it is unknown |

Rewrite:

> We chose the event-driven approach. The alternative couples the services tightly. The trade-off is latency: the consumer processes an event up to two seconds after the producer emits it.

The number was not in the original. Where you do not have it, write "The trade-off is latency, which we have not yet measured" rather than leaving *some implications* to stand.

## Error message

Original:

> Invalid configuration.

| Rule violated | Fix |
| ------------- | --- |
| Ellipsis — no subject, no verb | Restore both |
| No cause and no action | State what failed and what to do |

Rewrite:

> The server did not start. The field `timeout_seconds` in /etc/app.yaml is "30s", but this field must be an integer. Set it to 30.

## Tool description

Original:

> Handles user data processing tasks and related operations for the pipeline.

| Rule violated | Fix |
| ------------- | --- |
| Noun cluster of four words (*user data processing tasks*) | Break it apart |
| Vague verbs (*handles*, *related operations*) | Name the action |
| No stated input or output | State both |

Rewrite:

> Reads a user record from the ingest queue. Removes personal fields. Writes the result to the analytics table. Returns the number of records written.

## Compliant text left unchanged

Original:

> Run `just migrate` before you start the server. The migration takes about 30 seconds.

No violations. Two simple sentences, active voice, simple tenses, condition stated first. Report it as compliant and change nothing.

## A rewrite that was correctly refused

Original:

> Do not run this command against production unless you have confirmed with the data owner that the affected rows are recoverable from the previous night's snapshot.

The sentence runs to 28 words, over the 20-word procedural limit. Splitting it is fine, but dropping either qualifier is not: *confirmed with the data owner* and *recoverable from the previous night's snapshot* are both load-bearing safety conditions.

Rewrite that keeps every condition:

> **Warning:** This command can delete rows that you cannot recover.
>
> Before you run this command against production:
>
> 1. Confirm with the data owner that the affected rows are in last night's snapshot.
> 2. Run the command only after the data owner confirms this.

Flag in the note: the sentence was split rather than shortened, because both conditions are required.
