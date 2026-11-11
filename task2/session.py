"""Finite-state model of a three-consecutive-failure card lockout policy."""


def run_session(events: str) -> tuple[str, tuple[str, ...]]:
    """Consume C (correct) / W (wrong) events; return final state and trace.

    A correct attempt resets the failure count. Three consecutive wrong
    attempts move to LOCKED, which is absorbing for every later event.
    """
    state = "READY"
    trace = [state]
    for event in events:
        if event not in {"C", "W"}:
            raise ValueError("Session events must be C (correct) or W (wrong).")
        if state == "LOCKED":
            trace.append(state)
            continue
        if event == "C":
            state = "READY"
        elif event == "W":
            state = {"READY": "ONE_WRONG", "ONE_WRONG": "TWO_WRONG", "TWO_WRONG": "LOCKED"}[state]
        trace.append(state)
    return state, tuple(trace)

