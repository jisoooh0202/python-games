"""Tests for the terminal Color Puzzle rules."""

import unittest

from games.color_puzzle.model import (
    DIFFICULTIES,
    ColorPuzzleBoard,
    InvalidMove,
    is_solvable,
)
from games.color_puzzle.game import ColorPuzzleGame


class ColorPuzzleBoardTest(unittest.TestCase):
    def test_pour_moves_contiguous_matching_color(self):
        board = ColorPuzzleBoard([["R", "G", "G"], ["G"], []], capacity=4)

        amount = board.pour(0, 1)

        self.assertEqual(amount, 2)
        self.assertEqual(board.tubes, [["R"], ["G", "G", "G"], []])
        self.assertEqual(board.moves, 1)

    def test_cannot_pour_onto_different_color(self):
        board = ColorPuzzleBoard([["R"], ["B"], []], capacity=4)

        with self.assertRaises(InvalidMove):
            board.pour(0, 1)

    def test_undo_restores_last_pour(self):
        board = ColorPuzzleBoard([["R", "R"], [], ["B"]], capacity=4)
        board.pour(0, 1)

        self.assertTrue(board.undo())

        self.assertEqual(board.tubes, [["R", "R"], [], ["B"]])
        self.assertEqual(board.moves, 0)

    def test_solved_requires_full_single_color_tubes(self):
        solved = ColorPuzzleBoard([["R"] * 4, ["B"] * 4, []], capacity=4)
        partial = ColorPuzzleBoard([["R", "R"], ["B"] * 4, []], capacity=4)

        self.assertTrue(solved.is_solved())
        self.assertFalse(partial.is_solved())

    def test_generated_board_is_solvable(self):
        board = ColorPuzzleBoard.new(seed=7)

        self.assertFalse(board.is_solved())
        self.assertTrue(is_solvable(board.snapshot(), board.capacity))

    def test_has_seven_named_difficulty_levels(self):
        self.assertEqual(
            [difficulty.name for difficulty in DIFFICULTIES],
            ["easiest", "easier", "easy", "normal", "hard", "harder", "hardest"],
        )

    def test_difficulty_controls_board_size(self):
        difficulty = DIFFICULTIES[0]

        board = ColorPuzzleBoard.for_difficulty(difficulty, seed=3)

        self.assertEqual(len(board.tubes), difficulty.color_count + difficulty.empty_tubes)

    def test_level_can_change_with_plus_and_minus_keys(self):
        game = ColorPuzzleGame(seed=5)
        starting_level = game.level_index

        game._handle_key(ord("+"))
        self.assertEqual(game.level_index, starting_level + 1)

        game._handle_key(ord("-"))
        self.assertEqual(game.level_index, starting_level)


if __name__ == "__main__":
    unittest.main()
