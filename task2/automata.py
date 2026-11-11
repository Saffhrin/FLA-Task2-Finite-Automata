"""Small reusable DFA and NFA recognizers."""
from dataclasses import dataclass
from typing import Callable, FrozenSet, Hashable

State = Hashable


@dataclass(frozen=True)
class DFA:
    start: State
    accepting: FrozenSet[State]
    transition: Callable[[State, str], State]

    def run(self, value: str) -> tuple[bool, list[State]]:
        state = self.start
        path = [state]
        for symbol in value:
            state = self.transition(state, symbol)
            path.append(state)
        return state in self.accepting, path


@dataclass(frozen=True)
class NFA:
    start: State
    accepting: FrozenSet[State]
    transition: Callable[[State, str], FrozenSet[State]]

    def run(self, value: str) -> tuple[bool, list[FrozenSet[State]]]:
        states: FrozenSet[State] = frozenset({self.start})
        path = [states]
        for symbol in value:
            states = frozenset(
                target for state in states
                for target in self.transition(state, symbol)
            )
            path.append(states)
        return bool(states & self.accepting), path
