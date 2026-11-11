"""Small reusable DFA and NFA recognizers."""
from dataclasses import dataclass
from collections import deque
from typing import Callable, FrozenSet, Hashable, Iterable

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

    def reachable_states(self, alphabet: Iterable[str]) -> FrozenSet[State]:
        """Enumerate states reachable from the start over a finite alphabet."""
        states = {self.start}
        pending = deque([self.start])
        symbols = tuple(alphabet)
        while pending:
            state = pending.popleft()
            for symbol in symbols:
                target = self.transition(state, symbol)
                if target not in states:
                    states.add(target)
                    pending.append(target)
        return frozenset(states)

    def minimize(
        self,
        alphabet: Iterable[str],
        classify: Callable[[str], str] = lambda symbol: symbol,
    ) -> "DFA":
        """Return the reachable DFA quotient under partition refinement."""
        symbols = tuple(alphabet)
        states = self.reachable_states(symbols)
        accepting = states & self.accepting
        partitions = [part for part in (accepting, states - accepting) if part]
        while True:
            block_of = {state: i for i, block in enumerate(partitions) for state in block}
            groups: dict[tuple[bool, tuple[int, ...]], set[State]] = {}
            for state in states:
                signature = (
                    state in accepting,
                    tuple(block_of[self.transition(state, symbol)] for symbol in symbols),
                )
                groups.setdefault(signature, set()).add(state)
            refined = [frozenset(group) for group in groups.values()]
            if {frozenset(block) for block in refined} == {frozenset(block) for block in partitions}:
                partitions = refined
                break
            partitions = refined

        block_of = {state: block for block in partitions for state in block}
        transitions: dict[tuple[FrozenSet[State], str], FrozenSet[State]] = {}
        for block in partitions:
            representative = next(iter(block))
            for symbol in symbols:
                transitions[(block, symbol)] = block_of[self.transition(representative, symbol)]
        return DFA(
            start=block_of[self.start],
            accepting=frozenset(block for block in partitions if block & accepting),
            transition=lambda block, char: transitions[(block, classify(char))],
        )


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

    def to_dfa(
        self,
        alphabet: Iterable[str],
        classify: Callable[[str], str] = lambda symbol: symbol,
    ) -> DFA:
        """Build the reachable subset-construction DFA over representative symbols.

        `classify` maps each real input character to one symbol in `alphabet`.
        The caller supplies one representative for every transition-equivalence
        class in the input alphabet.
        """
        symbols = tuple(alphabet)
        start = frozenset({self.start})
        transitions: dict[tuple[FrozenSet[State], str], FrozenSet[State]] = {}
        seen = {start}
        pending = deque([start])
        while pending:
            states = pending.popleft()
            for symbol in symbols:
                targets = frozenset(
                    target for state in states
                    for target in self.transition(state, symbol)
                )
                transitions[(states, symbol)] = targets
                if targets not in seen:
                    seen.add(targets)
                    pending.append(targets)
        accepting = frozenset(
            states for states in seen if states & self.accepting
        )
        return DFA(
            start=start,
            accepting=accepting,
            transition=lambda states, char: transitions[(states, classify(char))],
        )

    def reachable_subset_states(self, alphabet: Iterable[str]) -> FrozenSet[FrozenSet[State]]:
        """Return the reachable powerset states, including the empty dead set."""
        symbols = tuple(alphabet)
        return self.to_dfa(symbols).reachable_states(symbols)

