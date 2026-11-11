# Task 2 — Finite Automata for Input Validation

An individual Python project demonstrating DFA and NFA recognition for password policy checks, a deliberately limited email format, and four-digit ATM PIN format.

## Scope

This project follows the Task 2 topics and report criteria recovered from the referenced conversation. The original faculty assignment PDF was not attached there, so confirm the final scope against your course brief before submission. This is an original implementation; the attached student report was used only as contextual reference.

## Requirements and run

Python 3.10 or newer; no third-party packages are needed.

```bash
python -m task2
```

Choose a validator from the menu and enter a value. Run the automated test suite with:

```bash
python -m unittest discover -s tests -v
```

## Models

* **Password:** DFA state is `(length, U, L, D, S)`, where length is capped at 8 and the flags record uppercase, lowercase, digit, and ASCII non-alphanumeric presence. Accept iff length ≥ 8 and all flags are set. This is a finite product automaton with 9 × 16 states (including unreachable combinations).
* **Email subset:** NFA for `ALNUM+ @ ALNUM+ . LETTER{2,}`. The NFA consumes the local part and domain, then nondeterministically selects a dot in the domain as the separator before a 2+ letter suffix. This intentionally small format subset does not claim to implement the full email standards.
* **ATM PIN:** DFA with states for 0–4 digits plus a dead state; only the state after exactly four ASCII digits accepts.

See [`docs/design.md`](docs/design.md) for transition diagrams, formal definitions, test vectors, limitations, and report-ready content.

## Structure

```text
task2/       automata and validators
tests/       standard-library unittest suite
docs/        formal design and report content
```

The validators check syntax only. Password acceptance is not a security-strength rating, email acceptance does not prove mailbox existence, and PIN acceptance does not authenticate a bank account.

Repository: https://github.com/Saffhrin/FLA-Task2-Finite-Automata

