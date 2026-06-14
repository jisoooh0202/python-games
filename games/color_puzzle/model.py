"""Game rules and puzzle generation for Color Puzzle."""

from __future__ import annotations

from collections import deque
import random
from dataclasses import dataclass, field


DEFAULT_CAPACITY = 4
DEFAULT_COLOR_COUNT = 4
DEFAULT_EMPTY_TUBES = 2
DEFAULT_SOLVER_LIMIT = 200_000
COLORS = ("R", "G", "B", "Y", "M", "C", "O", "P")


@dataclass(frozen=True)
class Difficulty:
    """Puzzle size settings for a named level."""

    name: str
    color_count: int
    empty_tubes: int
    solver_limit: int = DEFAULT_SOLVER_LIMIT
    scramble_moves: int = 10
    max_initial_run: int | None = None


DIFFICULTIES = (
    Difficulty("easiest", 2, 3, 20_000, 5),
    Difficulty("easier", 2, 2, 25_000, 7),
    Difficulty("easy", 3, 3, 35_000, 9),
    Difficulty("normal", 4, 3, 60_000, 12),
    Difficulty("hard", 5, 3, 90_000, 15),
    Difficulty("harder", 6, 3, 120_000, 18, 2),
    Difficulty("hardest", 7, 3, 160_000, 21, 2),
)
DEFAULT_DIFFICULTY_INDEX = 3


class InvalidMove(ValueError):
    """Raised when a requested pour is not allowed."""


@dataclass
class ColorPuzzleBoard:
    """Mutable color sorting board.

    Tubes are stored from bottom to top. The last value in a tube is the
    currently pourable color.
    """

    tubes: list[list[str]]
    capacity: int = DEFAULT_CAPACITY
    moves: int = 0
    history: list[tuple[int, int, int, str]] = field(default_factory=list)

    @classmethod
    def new(
        cls,
        color_count: int = DEFAULT_COLOR_COUNT,
        empty_tubes: int = DEFAULT_EMPTY_TUBES,
        capacity: int = DEFAULT_CAPACITY,
        seed: int | None = None,
        solver_limit: int = DEFAULT_SOLVER_LIMIT,
        scramble_moves: int | None = None,
        max_initial_run: int | None = None,
    ) -> "ColorPuzzleBoard":
        """Create a randomized, solver-checked board."""
        rng = random.Random(seed)
        return generate_board(
            color_count,
            empty_tubes,
            capacity,
            rng,
            solver_limit,
            scramble_moves,
            max_initial_run,
        )

    @classmethod
    def for_difficulty(
        cls,
        difficulty: Difficulty,
        capacity: int = DEFAULT_CAPACITY,
        seed: int | None = None,
    ) -> "ColorPuzzleBoard":
        """Create a randomized board for a named difficulty."""
        return cls.new(
            color_count=difficulty.color_count,
            empty_tubes=difficulty.empty_tubes,
            capacity=capacity,
            seed=seed,
            solver_limit=difficulty.solver_limit,
            scramble_moves=difficulty.scramble_moves,
            max_initial_run=difficulty.max_initial_run,
        )

    def snapshot(self) -> tuple[tuple[str, ...], ...]:
        """Return a hashable board state."""
        return tuple(tuple(tube) for tube in self.tubes)

    def is_solved(self) -> bool:
        """Return True when every non-empty tube contains one full color."""
        for tube in self.tubes:
            if not tube:
                continue
            if len(tube) != self.capacity or len(set(tube)) != 1:
                return False
        return True

    def top_color(self, index: int) -> str | None:
        """Return the top color of a tube."""
        tube = self.tubes[index]
        return tube[-1] if tube else None

    def can_pour(self, source: int, target: int) -> bool:
        """Return True if source can pour into target."""
        if source == target:
            return False

        source_tube = self.tubes[source]
        target_tube = self.tubes[target]
        if not source_tube or len(target_tube) >= self.capacity:
            return False
        if target_tube and target_tube[-1] != source_tube[-1]:
            return False
        return True

    def pour_amount(self, source: int, target: int) -> int:
        """Return how many color units would pour for a valid move."""
        if not self.can_pour(source, target):
            return 0

        source_tube = self.tubes[source]
        target_tube = self.tubes[target]
        color = source_tube[-1]
        contiguous = 0

        for value in reversed(source_tube):
            if value != color:
                break
            contiguous += 1

        return min(contiguous, self.capacity - len(target_tube))

    def pour(self, source: int, target: int) -> int:
        """Pour from source into target and return the amount poured."""
        if source < 0 or source >= len(self.tubes) or target < 0 or target >= len(self.tubes):
            raise InvalidMove("Tube number out of range.")

        amount = self.pour_amount(source, target)
        if amount == 0:
            raise InvalidMove("You can only pour onto the same color or into an empty tube.")

        color = self.tubes[source][-1]
        for _ in range(amount):
            self.tubes[target].append(self.tubes[source].pop())

        self.moves += 1
        self.history.append((source, target, amount, color))
        return amount

    def undo(self) -> bool:
        """Undo the last pour. Return False if there is nothing to undo."""
        if not self.history:
            return False

        source, target, amount, _color = self.history.pop()
        for _ in range(amount):
            self.tubes[source].append(self.tubes[target].pop())
        self.moves = max(0, self.moves - 1)
        return True


def legal_moves(state: tuple[tuple[str, ...], ...], capacity: int) -> list[tuple[int, int]]:
    """Return legal pours for an immutable board state."""
    moves = []
    for source, source_tube in enumerate(state):
        if not source_tube:
            continue

        source_color = source_tube[-1]
        for target, target_tube in enumerate(state):
            if source == target or len(target_tube) >= capacity:
                continue
            if target_tube and target_tube[-1] != source_color:
                continue
            moves.append((source, target))

    return moves


def apply_move(
    state: tuple[tuple[str, ...], ...], source: int, target: int, capacity: int
) -> tuple[tuple[str, ...], ...]:
    """Apply a legal move to an immutable board state."""
    tubes = [list(tube) for tube in state]
    color = tubes[source][-1]
    amount = 0

    for value in reversed(tubes[source]):
        if value != color:
            break
        amount += 1

    amount = min(amount, capacity - len(tubes[target]))
    for _ in range(amount):
        tubes[target].append(tubes[source].pop())

    return tuple(tuple(tube) for tube in tubes)


def is_solved_state(state: tuple[tuple[str, ...], ...], capacity: int) -> bool:
    """Return True if an immutable board state is solved."""
    for tube in state:
        if not tube:
            continue
        if len(tube) != capacity or len(set(tube)) != 1:
            return False
    return True


def longest_run(tube: tuple[str, ...] | list[str]) -> int:
    """Return the longest consecutive run in a tube."""
    best = 0
    current = 0
    previous = None

    for color in tube:
        if color == previous:
            current += 1
        else:
            current = 1
            previous = color
        best = max(best, current)

    return best


def has_long_initial_run(state: tuple[tuple[str, ...], ...], max_initial_run: int) -> bool:
    """Return True when a tube has too many matching colors in a row."""
    return any(longest_run(tube) > max_initial_run for tube in state)


def is_solvable(
    state: tuple[tuple[str, ...], ...],
    capacity: int,
    node_limit: int = DEFAULT_SOLVER_LIMIT,
) -> bool:
    """Check whether a board can be solved within a bounded BFS search."""
    queue = deque([state])
    seen = {state}

    while queue and len(seen) <= node_limit:
        current = queue.popleft()
        if is_solved_state(current, capacity):
            return True

        for source, target in legal_moves(current, capacity):
            next_state = apply_move(current, source, target, capacity)
            if next_state not in seen:
                seen.add(next_state)
                queue.append(next_state)

    return False


def generate_board(
    color_count: int,
    empty_tubes: int,
    capacity: int,
    rng: random.Random,
    solver_limit: int = DEFAULT_SOLVER_LIMIT,
    scramble_moves: int | None = None,
    max_initial_run: int | None = None,
) -> ColorPuzzleBoard:
    """Generate a solvable puzzle by scattering chunks from a solved board."""
    if color_count < 2:
        raise ValueError("color_count must be at least 2.")
    if color_count > len(COLORS):
        raise ValueError(f"color_count cannot exceed {len(COLORS)}.")
    if empty_tubes < 1:
        raise ValueError("empty_tubes must be at least 1.")
    if capacity < 2:
        raise ValueError("capacity must be at least 2.")

    moves_to_make = scramble_moves or max(6, color_count * 3)
    colors = COLORS[:color_count]

    for _ in range(1000):
        tubes = [[color] * capacity for color in colors]
        tubes.extend([] for _ in range(empty_tubes))
        moves_made = 0

        for _attempt in range(moves_to_make * 12):
            sources = [
                index
                for index, color in enumerate(colors)
                if tubes[index] and all(value == color for value in tubes[index])
            ]
            sources = [
                index
                for index in sources
                if any(target != index and len(tubes[target]) < capacity for target in range(len(tubes)))
            ]
            if not sources:
                break

            source = rng.choice(sources)
            targets = [
                index
                for index, tube in enumerate(tubes)
                if index != source and len(tube) < capacity
            ]
            target = rng.choice(targets)
            amount = rng.randint(1, min(len(tubes[source]), capacity - len(tubes[target])))

            for _ in range(amount):
                tubes[target].append(tubes[source].pop())
            moves_made += 1

            if moves_made >= moves_to_make:
                break

        rng.shuffle(tubes)
        state = tuple(tuple(tube) for tube in tubes)
        if moves_made < max(2, moves_to_make // 2):
            continue
        if is_solved_state(state, capacity):
            continue
        if max_initial_run is not None and has_long_initial_run(state, max_initial_run):
            continue

        return ColorPuzzleBoard([list(tube) for tube in state], capacity)

    raise RuntimeError("Could not generate a solvable Color Puzzle board.")
