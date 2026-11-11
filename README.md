# Finite Automata for Real-Time Input Validation

An individual Python project applying DFA/NFA models to password policy checks, practical email-format validation, and four-digit ATM PIN format. It includes a three-strike session model as an extra case study, traceable command-line runs, and a standalone browser demo.

## Scope

This project follows the Task 2 topics and report criteria recovered from the referenced conversation. The original faculty assignment PDF was not attached there, so confirm the final scope against your course brief before submission. This is an original implementation; the attached student report was used only as contextual reference.

## Requirements and run

Python 3.10 or newer; no third-party packages are needed.

```bash
python -m task2
```

Choose a validator from the menu. Additional model summaries are available with:

```bash
python -m task2 --stats
python -m task2 --limits
```

Open [`docs/index.html`](docs/index.html) locally for the interactive browser demo. The Python code is the implementation source; the static demo provides a second way to explore state traces.

Run the standard-library test suite with:

```bash
python -m unittest discover -s tests -v
```

## Models

| Case | Formal model | Demonstration |
|---|---|---|
| Password policy | Product DFA tracks capped length and four character-class flags | Per-character `(length, mask)` trace |
| Email format | Explicit NFA with a true branch at each candidate domain dot; subset construction and partition-refinement minimization produce DFAs | NFA active-state trace and NFA/DFA agreement cases |
| ATM PIN | DFA recognizes exactly four ASCII digits | State-by-state digit counter with a dead state |
| Attempt lockout | Separate DFA over `C`orrect / `W`rong attempt events; locks after three consecutive failures | Session trace, including reset and absorbing lock state |

The email subset is specified in [`docs/design.md`](docs/design.md). It allows alphanumeric local/domain labels, local separators `._-`, domain hyphens, subdomains, and a 2+ letter final suffix. It does not claim full standards compliance.

See [`docs/design.md`](docs/design.md) for the formal definitions, transition diagrams/tables, accepted and rejected examples, derivations, limitations, and report-ready content. The same document is the individual report draft.

## Structure

```text
task2/       DFA/NFA engine, validators, and session DFA
tests/       standard-library cases plus exhaustive short-string NFA/DFA agreement checks
docs/        report, Mermaid diagrams, JSON model manifest, and browser demo
```

## Scope limits

The models recognize formats and event sequences. Password acceptance is not a strength score; email acceptance does not prove that a mailbox exists; PIN format acceptance does not authenticate a bank account; and the session DFA is not a real banking system.

Repository: https://github.com/Saffhrin/FLA-Task2-Finite-Automata

