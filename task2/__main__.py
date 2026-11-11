import argparse

from .session import run_session
from .validators import EMAIL_CLASSES, EMAIL_DFA, EMAIL_MIN_DFA, validate_email, validate_password, validate_pin


def main() -> None:
    parser = argparse.ArgumentParser(description="DFA/NFA demonstrations for input validation")
    parser.add_argument("--stats", action="store_true", help="show model state counts")
    parser.add_argument("--limits", action="store_true", help="show what format checks do not establish")
    args = parser.parse_args()
    if args.stats:
        print("Password product DFA: 9 × 16 = 144 possible states (some unreachable)")
        print(f"Email NFA subset DFA: {len(EMAIL_DFA.reachable_states(EMAIL_CLASSES))} reachable states")
        print(f"Email minimized DFA: {len(EMAIL_MIN_DFA.reachable_states(EMAIL_CLASSES))} states")
        print("Four-digit PIN DFA: 6 states (q0–q4 plus dead)")
        print("Three-strike session DFA: 4 states")
        return
    if args.limits:
        print("Password: checks the stated composition rule, not entropy or leaked-password exposure.")
        print("Email: checks the implemented ASCII format subset, not mailbox existence or deliverability.")
        print("PIN: checks four ASCII digits, not identity, bank records, or account status.")
        print("Session DFA: models a consecutive-failure policy, not an actual bank/card system.")
        return
    checks = {
        "1": ("Password", validate_password),
        "2": ("Email subset", validate_email),
        "3": ("Four-digit ATM PIN", validate_pin),
    }
    while True:
        print("\nFinite Automata Input Validator\n1) Password\n2) Email format subset\n3) ATM PIN format\n4) Three-strike session DFA\nq) Quit")
        choice = input("> ").strip().lower()
        if choice == "q":
            return
        if choice == "4":
            events = input("Attempt events (C=correct, W=wrong; e.g. WWCWW): ").strip().upper()
            try:
                state, trace = run_session(events)
                print(f"Final state: {state}\nTrace: {' → '.join(trace)}")
            except ValueError as exc:
                print(f"Invalid event sequence: {exc}")
            continue
        if choice not in checks:
            print("Choose 1, 2, 3, 4, or q.")
            continue
        label, checker = checks[choice]
        value = input(f"{label}: ")
        print("ACCEPTED" if checker(value) else "REJECTED")


if __name__ == "__main__":
    main()

