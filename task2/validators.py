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
    if state == "local_start" and alnum:
        moves.add("local_word")
    elif state == "local_word":
        if alnum:
            moves.add("local_word")
        elif char in "._-":
            moves.add("local_need_alnum")
        elif char == "@":
            moves.add("domain_start")
    elif state == "local_need_alnum" and alnum:
        moves.add("local_word")
    elif state == "domain_start" and alnum:
        moves.add("domain_word")
    elif state == "domain_word":
        if alnum:
            moves.add("domain_word")
        elif char == "-":
            moves.add("domain_need_alnum")
        elif char == ".":
            # This is the true NFA choice: continue with another domain label,
            # or guess that this dot begins the alphabetic final suffix.
            moves.update({"domain_after_dot", "tld_first"})
    elif state in {"domain_need_alnum", "domain_after_dot"} and alnum:
        moves.add("domain_word")
    elif state == "tld_first" and letter:
        moves.add("tld_one")
    elif state == "tld_one" and letter:
        moves.add("tld_accept")
    elif state == "tld_accept" and letter:
        moves.add("tld_accept")
    return frozenset(moves)


EMAIL_NFA = NFA("local_start", frozenset({"tld_accept"}), _email_transition)
EMAIL_CLASSES = ("a", "0", ".", "_", "-", "@", "!")


def _email_class(char: str) -> str:
    if char.isascii() and char.isalpha():
        return "a"
    if char.isascii() and char.isdigit():
        return "0"
    return char if char in {".", "_", "-", "@"} else "!"


EMAIL_DFA = EMAIL_NFA.to_dfa(EMAIL_CLASSES, _email_class)
EMAIL_MIN_DFA = EMAIL_DFA.minimize(EMAIL_CLASSES, _email_class)


def validate_password(value: str) -> bool:
    return PASSWORD_DFA.run(value)[0]


def validate_email(value: str) -> bool:
    return EMAIL_NFA.run(value)[0]


def validate_email_dfa(value: str) -> bool:
    return EMAIL_DFA.run(value)[0]


def validate_email_min_dfa(value: str) -> bool:
    return EMAIL_MIN_DFA.run(value)[0]


def validate_pin(value: str) -> bool:
    return PIN_DFA.run(value)[0]

