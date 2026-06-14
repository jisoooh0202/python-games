"""Keyboard-only terminal UI for Color Puzzle."""

from __future__ import annotations

import curses
import random
import time

from .model import (
    COLORS,
    DEFAULT_DIFFICULTY_INDEX,
    DIFFICULTIES,
    ColorPuzzleBoard,
    InvalidMove,
)


COLOR_NAMES = {
    "R": "red",
    "G": "green",
    "B": "blue",
    "Y": "yellow",
    "M": "magenta",
    "C": "cyan",
    "O": "orange",
    "P": "purple",
}

CURSES_COLORS = {
    "R": curses.COLOR_RED,
    "G": curses.COLOR_GREEN,
    "B": curses.COLOR_BLUE,
    "Y": curses.COLOR_YELLOW,
    "M": curses.COLOR_MAGENTA,
    "C": curses.COLOR_CYAN,
    "O": curses.COLOR_WHITE,
    "P": curses.COLOR_MAGENTA,
}


class ColorPuzzleGame:
    """Interactive terminal Color Puzzle game."""

    def __init__(self, seed: int | None = None, level_index: int = DEFAULT_DIFFICULTY_INDEX):
        self.seed = seed
        self.level_index = level_index
        self.board = self._new_board()
        self.cursor = 0
        self.selected: int | None = None
        self.celebrate_pending = False
        self.message = "Select a tube, then choose where to pour."
        self.message_until = 0.0

    @property
    def difficulty(self):
        """Return the current difficulty settings."""
        return DIFFICULTIES[self.level_index]

    def _new_board(self):
        return ColorPuzzleBoard.for_difficulty(self.difficulty, seed=self.seed)

    def run(self):
        """Start the curses app."""
        curses.wrapper(self._run)

    def _run(self, stdscr):
        curses.curs_set(0)
        stdscr.keypad(True)
        curses.use_default_colors()
        self._init_colors()

        while True:
            self._draw(stdscr)
            key = stdscr.getch()
            if not self._handle_key(key):
                break
            if self.celebrate_pending:
                self.celebrate_pending = False
                self._play_fireworks(stdscr)

    def _init_colors(self):
        if not curses.has_colors():
            return

        curses.start_color()
        for index, color in enumerate(COLORS, start=1):
            curses.init_pair(index, CURSES_COLORS[color], -1)
        curses.init_pair(len(COLORS) + 1, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(len(COLORS) + 2, curses.COLOR_BLACK, curses.COLOR_CYAN)

    def _handle_key(self, key: int) -> bool:
        if key in (ord("q"), ord("Q"), 27):
            return False
        if key in (curses.KEY_LEFT, ord("h"), ord("H")):
            self.cursor = (self.cursor - 1) % len(self.board.tubes)
        elif key in (curses.KEY_RIGHT, ord("l"), ord("L")):
            self.cursor = (self.cursor + 1) % len(self.board.tubes)
        elif key in (curses.KEY_HOME,):
            self.cursor = 0
        elif key in (curses.KEY_END,):
            self.cursor = len(self.board.tubes) - 1
        elif key in (ord("\n"), ord(" "), curses.KEY_ENTER):
            self._select_or_pour()
        elif key in (ord("u"), ord("U")):
            if self.board.undo():
                self.selected = None
                self._set_message("Undid the last pour.")
            else:
                self._set_message("Nothing to undo.")
        elif key in (ord("r"), ord("R")):
            self.board = self._new_board()
            self.cursor = 0
            self.selected = None
            self._set_message("Restarted with a fresh puzzle.")
        elif key in (ord("n"), ord("N")):
            self.seed = None
            self.board = self._new_board()
            self.cursor = 0
            self.selected = None
            self._set_message(f"New {self.difficulty.name} puzzle ready.")
        elif key in (ord("["), ord("{"), ord("-"), ord("_"), ord(","), ord("<")):
            self._change_level(-1)
        elif key in (ord("]"), ord("}"), ord("+"), ord("="), ord("."), ord(">"), ord("/")):
            self._change_level(1)
        elif ord("1") <= key <= ord("9"):
            index = key - ord("1")
            if index < len(self.board.tubes):
                self.cursor = index
                self._select_or_pour()

        return True

    def _change_level(self, step: int):
        next_index = min(max(self.level_index + step, 0), len(DIFFICULTIES) - 1)
        if next_index == self.level_index:
            self._set_message(f"Already on {self.difficulty.name}.")
            return

        self.level_index = next_index
        self.seed = None
        self.board = self._new_board()
        self.cursor = 0
        self.selected = None
        self._set_message(f"Level changed to {self.difficulty.name}.")

    def _select_or_pour(self):
        if self.board.is_solved():
            self._set_message("Puzzle already solved. Press N for another one.")
            return

        if self.selected is None:
            if not self.board.tubes[self.cursor]:
                self._set_message("That tube is empty. Pick a color tube first.")
                return
            self.selected = self.cursor
            self._set_message(f"Holding tube {self.cursor + 1}. Choose where to pour.")
            return

        source = self.selected
        target = self.cursor

        if source == target:
            self._set_message(f"Still holding tube {source + 1}. Move to another tube to pour.")
            return

        self.selected = None

        try:
            amount = self.board.pour(source, target)
        except InvalidMove as error:
            self._set_message(str(error))
            return

        plural = "" if amount == 1 else "s"
        if self.board.is_solved():
            self._set_message(f"Solved in {self.board.moves} moves. Press N for another puzzle.", sticky=True)
            self.celebrate_pending = True
        else:
            self._set_message(f"Poured {amount} block{plural}.")

    def _set_message(self, message: str, sticky: bool = False):
        self.message = message
        self.message_until = 0.0 if sticky else time.time() + 3.5

    def _draw(self, stdscr):
        stdscr.erase()
        height, width = stdscr.getmaxyx()

        if height < 16 or width < 54:
            stdscr.addstr(0, 0, "Make the terminal at least 54x16 to play Color Puzzle.")
            stdscr.refresh()
            return

        title = "ColorPuzzleGame"
        stdscr.addstr(0, max(0, (width - len(title)) // 2), title, curses.A_BOLD)
        stdscr.addstr(1, 2, f"Moves: {self.board.moves}")
        level_text = f"Level: {self.difficulty.name}"
        stdscr.addstr(1, max(2, width - len(level_text) - 2), level_text, curses.A_BOLD)

        controls = "Arrows/H-L move  Enter/Space select  1-9 pick  U undo  -/+ level  N new  Q quit"
        stdscr.addstr(2, 2, controls[: width - 4])

        if self.selected is not None:
            holding = f"HOLDING TUBE {self.selected + 1} -> choose destination"
            attr = curses.A_BOLD | curses.A_REVERSE
            if curses.has_colors():
                attr |= curses.color_pair(len(COLORS) + 2)
            stdscr.addstr(3, 2, holding[: width - 4], attr)

        if self.message_until and time.time() > self.message_until:
            self.message = "Select a tube, then choose where to pour."
            self.message_until = 0.0
        stdscr.addstr(4, 2, self.message[: width - 4], curses.A_DIM)

        start_y = 6
        tube_width = 7
        total_width = len(self.board.tubes) * tube_width
        start_x = max(2, (width - total_width) // 2)

        for index, tube in enumerate(self.board.tubes):
            x = start_x + index * tube_width
            self._draw_tube(stdscr, start_y, x, index, tube)

        stdscr.refresh()

    def _draw_tube(self, stdscr, y: int, x: int, index: int, tube: list[str]):
        selected = index == self.selected
        focused = index == self.cursor
        if selected:
            y -= 1

        label_attr = curses.A_NORMAL
        if focused:
            label_attr |= curses.A_BOLD | curses.A_REVERSE
            if curses.has_colors():
                label_attr |= curses.color_pair(len(COLORS) + 1)
        if selected:
            label_attr |= curses.A_BOLD | curses.A_REVERSE
            if curses.has_colors():
                label_attr |= curses.color_pair(len(COLORS) + 2)

        label = f"[{index + 1}]" if focused else f" {index + 1} "
        stdscr.addstr(y, x + 1, label, label_attr)

        if selected:
            stdscr.addstr(y + 1, x, "HELD", label_attr)

        for row in range(self.board.capacity - 1, -1, -1):
            block_y = y + 2 + (self.board.capacity - 1 - row) if selected else y + 1 + (self.board.capacity - 1 - row)
            side = "!" if selected else "|"
            stdscr.addstr(block_y, x, side, label_attr if selected else curses.A_NORMAL)
            stdscr.addstr(block_y, x + 4, side, label_attr if selected else curses.A_NORMAL)

            if row < len(tube):
                color = tube[row]
                attr = curses.A_BOLD
                if curses.has_colors():
                    attr |= curses.color_pair(COLORS.index(color) + 1)
                stdscr.addstr(block_y, x + 1, color * 3, attr)
            else:
                stdscr.addstr(block_y, x + 1, "   ", curses.A_DIM)

        base_attr = curses.A_BOLD if focused else curses.A_NORMAL
        base_y = y + self.board.capacity + 2 if selected else y + self.board.capacity + 1
        stdscr.addstr(base_y, x, "+---+", base_attr)

        if tube:
            name = COLOR_NAMES.get(tube[-1], tube[-1])
            stdscr.addstr(base_y + 1, x, name[:5])

    def _play_fireworks(self, stdscr):
        """Show a short ASCII celebration after the puzzle is solved."""
        height, width = stdscr.getmaxyx()
        if height < 10 or width < 30:
            return

        rng = random.Random()
        particles = []
        chars = ["*", "+", "x", "."]
        color_pairs = list(range(1, min(len(COLORS), 6) + 1))

        for frame in range(28):
            self._draw(stdscr)
            message = "CONGRATULATIONS!"
            submessage = f"Solved in {self.board.moves} moves"
            msg_x = max(0, (width - len(message)) // 2)
            sub_x = max(0, (width - len(submessage)) // 2)
            stdscr.addstr(5, msg_x, message, curses.A_BOLD | curses.A_REVERSE)
            stdscr.addstr(6, sub_x, submessage, curses.A_BOLD)

            if frame % 5 == 0:
                center_x = rng.randint(6, max(6, width - 7))
                center_y = rng.randint(2, max(2, min(height - 6, 8)))
                for dx, dy in (
                    (-2, -1),
                    (-1, -2),
                    (0, -2),
                    (1, -2),
                    (2, -1),
                    (-2, 0),
                    (2, 0),
                    (-2, 1),
                    (-1, 2),
                    (0, 2),
                    (1, 2),
                    (2, 1),
                ):
                    particles.append(
                        {
                            "x": center_x,
                            "y": center_y,
                            "dx": dx,
                            "dy": dy,
                            "age": 0,
                            "char": rng.choice(chars),
                            "color": rng.choice(color_pairs),
                        }
                    )

            next_particles = []
            for particle in particles:
                x = particle["x"] + particle["dx"] * particle["age"]
                y = particle["y"] + particle["dy"] * particle["age"] // 2
                if 0 <= x < width - 1 and 0 <= y < height - 1 and particle["age"] < 6:
                    attr = curses.A_BOLD
                    if curses.has_colors():
                        attr |= curses.color_pair(particle["color"])
                    stdscr.addstr(y, x, particle["char"], attr)
                    particle["age"] += 1
                    next_particles.append(particle)
            particles = next_particles

            stdscr.refresh()
            time.sleep(0.07)
