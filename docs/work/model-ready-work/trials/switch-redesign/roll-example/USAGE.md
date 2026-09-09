# Handoff report

`handoff_report.py` reads one JSON work record and prints a read-only Markdown
handoff to standard output. It does not update the record or decide that a
project is complete from its task counts.

## Input

The input must be a JSON object with these fields:

- `project`: nonempty string
- `stage`: nonempty string
- `next_action`: nonempty string
- `tasks`: list of task objects

Each task must contain a nonempty, unique string `id`, a nonempty string
`title`, and a `status` equal to `done`, `active`, `blocked`, or `queued`.
All strings must be single-line; carriage returns and line feeds are rejected.
Whitespace-only strings are also rejected.

## Run

```sh
python3 handoff_report.py path/to/work-record.json
```

The report is written to standard output, so it can be viewed directly or
redirected to a separate file:

```sh
python3 handoff_report.py path/to/work-record.json > handoff.md
```

Invalid JSON, invalid record data, unreadable input, or an incorrect number of
arguments produces an error on standard error and exit status 2. A valid record
produces the report on standard output and exit status 0.

## Fictional example

This sample project and all of its tasks are fictional:

```json
{
  "project": "Lunar Greenhouse Demonstration",
  "stage": "Prototype review",
  "next_action": "Ask the habitat team to approve the fictional irrigation plan.",
  "tasks": [
    {
      "id": "demo-01",
      "title": "Draft the greenhouse layout",
      "status": "done"
    },
    {
      "id": "demo-02",
      "title": "Review the irrigation assumptions",
      "status": "active"
    },
    {
      "id": "demo-03",
      "title": "Receive the imaginary lunar soil shipment",
      "status": "blocked"
    },
    {
      "id": "demo-04",
      "title": "Schedule a fictional planting rehearsal",
      "status": "queued"
    }
  ]
}
```

The resulting Markdown groups tasks in Done, Active, Blocked, and Queued order
while preserving input order inside each group. Empty task groups are omitted,
and the supplied next action is always printed after the task groups. An empty
`tasks` list is valid.

## Tests

Run the standard-library test suite from this directory:

```sh
python3 -m unittest -v
```

## Limitations

- The tool reads one local JSON file per invocation; it does not fetch records,
  monitor work, or integrate with project-management services.
- It validates and reports the supplied state only. It does not verify that a
  task was actually completed, resolve blockers, or infer overall completion.
- Status names and their display order are fixed.
- Reports are Markdown text for terminal display or redirection; there is no
  HTML rendering, interactive interface, or output-file option.
- String fields are limited to one line, so multi-paragraph descriptions and
  next actions are not supported.
