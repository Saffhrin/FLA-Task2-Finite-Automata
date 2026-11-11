"""Three input validators represented by explicit finite automata."""
from .automata import DFA, NFA


def _password_step(state: tuple[int, int], char: str) -> tuple[int, int]:
    length, flags = state
    flags |= (1 if char.isascii() and char.isupper() else 0)
    flags |= (2 if char.isascii() and char.islower() else 0)
    flags |= (4 if char.isascii() and char.isdigit() else 0)
    flags |= (8 if char.isascii() and not char.isalnum() else 0)
    return min(8, length + 1), flags


PASSWORD_DFA = DFA(
    start=(0, 0),
    accepting=frozenset((8, mask) for mask in range(16) if mask == 15),
    transition=_password_step,
)


def _pin_step(state: int | str, char: str) -> int | str:
    if state == "dead" or not (char.isascii() and char.isdigit()):
        return "dead"
    return state + 1 if state < 4 else "dead"


PIN_DFA = DFA(0, frozenset({4}), _pin_step)


def _email_transition(state: str, char: str) -> frozenset[str]:
    alnum = char.isascii() and char.isalnum()
    letter = char.isascii() and char.isalpha()
    moves: set[str] = set()
    if state == "local" and alnum:
        moves.add("local")
    if state == "local" and char == "@":
        moves.add("domain")
    if state == "domain" and alnum:
        moves.add("domain")
    # Nondeterministically choose any domain dot as the suffix boundary.
    if state == "domain" and char == ".":
        moves.add("suffix_first")
    if state == "suffix_first" and letter:
        moves.add("suffix_more")
    if state == "suffix_more" and letter:
        moves.add("suffix_more")
    return frozenset(moves)


EMAIL_NFA = NFA("local", frozenset({"suffix_more"}), _email_transition)


def validate_password(value: str) -> bool:
    return PASSWORD_DFA.run(value)[0]


def validate_email(value: str) -> bool:
    return EMAIL_NFA.run(value)[0]


def validate_pin(value: str) -> bool:
    return PIN_DFA.run(value)[0]
