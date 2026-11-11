from .validators import validate_email, validate_password, validate_pin


def main() -> None:
    checks = {
        "1": ("Password", validate_password),
        "2": ("Email subset", validate_email),
        "3": ("Four-digit ATM PIN", validate_pin),
    }
    while True:
        print("\nFinite Automata Input Validator\n1) Password\n2) Email format subset\n3) ATM PIN\nq) Quit")
        choice = input("> ").strip().lower()
        if choice == "q":
            return
        if choice not in checks:
            print("Choose 1, 2, 3, or q.")
            continue
        label, checker = checks[choice]
        value = input(f"{label}: ")
        print("ACCEPTED" if checker(value) else "REJECTED")


if __name__ == "__main__":
    main()
