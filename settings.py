class Settings:
    def __init__(self):
        """initialize the game statistics settings"""
        # set screen
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_colour = None
        self.text_colour = (255, 255, 255)

        # set ship's speed
        self.ship_limit = 3

        # set bullet
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_colour = 'red'
        self.bullets_allowed = 3

        # alien settings
        self.fleet_drop_speed = 10

        # how quickly yhe game speeds up
        self.speedup_scale = 1.1

        # how quickly the alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 5
        """initialize settings that change through out the game"""
        self.bullet_speed = 7
        self.alien_speed = 4.0

        # fleet_direction of 1 represent right; -1 represent left
        self.fleet_direction = 1

        # scoring settings
        self.aliens_points = 50

    def increase_speed(self):
        """increase speed settings and alien point values"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.aliens_points = int(self.aliens_points * self.score_scale)
        print(self.aliens_points)

