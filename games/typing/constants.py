"""Constants specific to the Typing game."""

from shared.constants import BLACK, WHITE, GREEN, RED, YELLOW, CYAN

# Window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Game settings
FPS = 60
LIVES = 3

# Level progression
LEVEL_UP_SCORE = 30  # Points needed to advance to next level
MAX_LEVEL = 10

# Fall speed settings (pixels per frame)
BASE_FALL_SPEED = 1
SPEED_INCREASE_PER_LEVEL = 0.1

# Spawn rate settings (frames between spawns)
BASE_SPAWN_RATE = 120  # 2 seconds at 60 FPS
MIN_SPAWN_RATE = 30  # Fastest spawn rate

# Word settings
WORD_FONT_SIZE = 32
UI_FONT_SIZE = 24
TITLE_FONT_SIZE = 48

# Colors
BACKGROUND_COLOR = BLACK
WORD_COLOR = WHITE
TYPED_COLOR = GREEN
MISSED_COLOR = RED
UI_COLOR = CYAN
TITLE_COLOR = YELLOW

# Level word lists
LEVEL_WORDS = {
    1: ["a", "s", "d", "f", "j", "k", "l", "h", "g"],  # Home row letters
    2: ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],  # Top row
    3: ["z", "x", "c", "v", "b", "n", "m"],  # Bottom row
    4: [
        "a",
        "s",
        "d",
        "f",
        "j",
        "k",
        "l",
        "h",
        "g",
        "q",
        "w",
        "e",
        "r",
        "t",
        "y",
        "u",
        "i",
        "o",
        "p",
        "z",
        "x",
        "c",
        "v",
        "b",
        "n",
        "m",
    ],  # All letters
    5: ["at", "is", "it", "in", "on", "up", "go", "to", "me", "we"],  # Simple 2-letter words
    6: ["cat", "dog", "run", "fun", "sun", "car", "boy", "girl", "big", "red"],  # 3-letter words
    7: ["home", "game", "play", "time", "word", "good", "help", "work", "love", "life"],  # 4-letter words
    8: ["house", "water", "world", "study", "learn", "happy", "quick", "green", "music", "space"],  # 5-letter words
    9: [
        "python",
        "typing",
        "rocket",
        "planet",
        "wizard",
        "castle",
        "dragon",
        "knight",
        "jungle",
        "bridge",
    ],  # 6-letter words
    10: [
        "computer",
        "keyboard",
        "rainbow",
        "elephant",
        "mountain",
        "programming",
        "adventure",
        "champion",
    ],  # 7+ letter words
}

# Scoring
SCORE_PER_CHAR = 1
LEVEL_BONUS = 50
