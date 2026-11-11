"""Three input validators represented by explicit finite automata."""
from .automata import DFA, NFA, product_dfa


def _is_upper(char: str) -> bool:
    return char.isascii() and char.isupper()


def _is_lower(char: str) -> bool:
    return char.isascii() and char.islower()


def _is_digit(char: str) -> bool:
    return char.isascii() and char.isdigit()


def _is_special(char: str) -> bool:
    return char.isascii() and not char.isalnum()


def _length_step(state: int, _char: str) -> int:
    return min(8, state + 1)


def _flag_step(predicate):
    return lambda seen, char: seen or predicate(char)


_length_dfa = DFA(0, frozenset({8}), _length_step)
_upper_dfa = DFA(False, frozenset({True}), _flag_step(_is_upper))
_lower_dfa = DFA(False, frozenset({True}), _flag_step(_is_lower))
_digit_dfa = DFA(False, frozenset({True}), _flag_step(_is_digit))
_special_dfa = DFA(False, frozenset({True}), _flag_step(_is_special))

# Direct product: capped length × four independent category-seen automata.
PASSWORD_DFA = product_dfa(
    (_length_dfa, _upper_dfa, _lower_dfa, _digit_dfa, _special_dfa),
    (range(9), (False, True), (False, True), (False, True), (False, True)),
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
