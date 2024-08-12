import sys
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from button import Button
from score_board import ScoreBoard


class AlienInvasion:
    def __init__(self):
        pygame.init()

        self.settings = Settings()

        self.game_paused = False

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")

        # Load the background image
        self.game_background = pygame.image.load('images/galaxy.jpeg').convert()
        self.main_menu_background = pygame.image.load('images/menu_background.jpeg').convert()

        # Scale the background images to fit the screen
        self.game_background = pygame.transform.scale(
            self.game_background,
            (self.settings.screen_width, self.settings.screen_height)
        )
        self.main_menu_background = pygame.transform.scale(
            self.main_menu_background,
            (self.settings.screen_width, self.settings.screen_height)
        )

        # create an instance to store game statistics
        # create  a scoreboard
        self.stats = GameStats(self)
        self.sb = ScoreBoard(self)
        self.clock = pygame.time.Clock()

        self.ship = Ship(self, "images/ship.png")
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # start alien invasion in an inactive state
        self.game_active = False

        # make the play button
        self.play_button = Button(self,"Play")

    def run_game(self):
        while True:
            self._check_event()
            if self.game_active and not self.game_paused:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)

    def _check_event(self):
        """Respond to key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_ESCAPE:  # Move this to the correct section
            self.game_paused = not self.game_paused

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        """Update images on the screen and flip to the new screen."""
        if not self.game_active:
            # Draw the main menu background image
            self.screen.blit(self.main_menu_background, (0, 0))
            self.play_button.draw_button()
        else:
            # Draw the background image
            self.screen.blit(self.game_background, (0, 0))

            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.ship.blitme()
            self.aliens.draw(self.screen)
            # draw the score information
            self.sb.show_score()
            # draw the play button if the game is inactive
            if not self.game_active:
                self.play_button.draw_button()

        pygame.display.flip()

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _create_fleet(self):
        """Create the fleet of aliens with specified spacing."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # Adjust the spacing based on the screen width and alien size
        horizontal_spacing = 3 * alien_width
        vertical_spacing = 2 * alien_height

        current_x, current_y = alien_width*2, alien_height*2
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < self.settings.screen_width - 2 * alien_width:
                self._create_alien(current_x, current_y)
                current_x += horizontal_spacing
            current_x = alien_width *2
            current_y += vertical_spacing

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update the positions."""
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_alien_bottom()

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.aliens_points * len(aliens)

            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

            self.settings.increase_speed()
            #increase level
            self.stats.level +=1
            self.sb.prep_level()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # decrement ship left and update score board
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
    def _check_alien_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _check_play_button(self,mouse_pos):
        """start a new game when a player clicks play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)

        if button_clicked and not self.game_active:
            # reset the game settings
            self.settings.initialize_dynamic_settings()
            # reset the game statistics
            self.stats.reset_stats()
            self.sb.prep_score()
            self.bullets.empty()
            self.aliens.empty()
            self.sb.prep_level()
            self.sb.prep_ships()
            # create a new fleet and centre the ship
            self._create_fleet()
            self.ship.center_ship()
            self.game_active = True

            # hide the mouse cursor
            pygame.mouse.set_visible(False)

ai = AlienInvasion()
ai.run_game()
