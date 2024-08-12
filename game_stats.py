import os


class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()
        # Load the high score from a file
        self.high_score = self.load_high_score()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def load_high_score(self):
        """Load the high score from a file."""
        high_score_file = 'high_score.txt'
        if os.path.exists(high_score_file):
            with open(high_score_file, 'r') as file:
                try:
                    return int(file.read().strip())
                except ValueError:
                    return 0
        return 0

    def save_high_score(self):
        """Save the high score to a file."""
        high_score_file = 'high_score.txt'
        with open(high_score_file, 'w') as file:
            file.write(str(self.high_score))
