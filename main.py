import pygame
import random

class Game:
    def __init__(self):
        pygame.init()

        # Create a game window
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Shooter Game with Levels")

        # Set up the game clock for frame rate control
        self.clock = pygame.time.Clock()

        # Load assets
        self.font_small = pygame.font.Font(None, 36)

        # Game state variables
        self.running = True
        self.game_over = False

        # Background
        self.floor_tiles = [pygame.Surface((50, 50)) for _ in range(3)]
        for tile in self.floor_tiles:
            tile.fill((random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)))
        self.background = self.create_random_background(self.screen_width, self.screen_height, self.floor_tiles)

        # Player setup
        self.player = pygame.Rect(375, 500, 50, 50)
        self.player_color = (255, 0, 0)
        self.player_speed = 5
        self.player_health = 100

        # Bullets
        self.bullets = []
        self.bullet_color = (255, 255, 0)
        self.bullet_speed = 10

        # Enemies
        self.enemies = []
        self.enemy_color = (0, 0, 255)
        self.enemy_speed = 3
        self.spawn_timer = 0

        # XP and Levels
        self.xp = 0
        self.level = 1
        self.xp_to_next_level = 100

    def create_random_background(self, width, height, floor_tiles):
        bg = pygame.Surface((width, height))
        tile_w = floor_tiles[0].get_width()
        tile_h = floor_tiles[0].get_height()

        for y in range(0, height, tile_h):
            for x in range(0, width, tile_w):
                tile = random.choice(floor_tiles)
                bg.blit(tile, (x, y))

        return bg

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()

    def handle_events(self):
        """Process user input (keyboard, mouse, quitting)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.x -= self.player_speed
        if keys[pygame.K_RIGHT]:
            self.player.x += self.player_speed
        if keys[pygame.K_UP]:
            self.player.y -= self.player_speed
        if keys[pygame.K_DOWN]:
            self.player.y += self.player_speed

        # Shooting bullets
        if keys[pygame.K_SPACE]:
            self.shoot_bullet()

    def shoot_bullet(self):
        """Shoot a bullet from the player's position."""
        bullet = pygame.Rect(self.player.centerx - 5, self.player.top, 10, 20)
        self.bullets.append(bullet)

    def spawn_enemy(self):
        """Spawn a new enemy at a random position at the top of the screen."""
        enemy = pygame.Rect(random.randint(0, self.screen_width - 50), 0, 50, 50)
        self.enemies.append(enemy)

    def update(self):
        """Update the game state."""
        # Keep the player within the screen bounds
        self.player.x = max(0, min(self.player.x, self.screen_width - self.player.width))
        self.player.y = max(0, min(self.player.y, self.screen_height - self.player.height))

        # Update bullets
        for bullet in self.bullets[:]:
            bullet.y -= self.bullet_speed
            if bullet.bottom < 0:
                self.bullets.remove(bullet)

        # Spawn enemies
        self.spawn_timer += 1
        if self.spawn_timer > 60:  # Spawn an enemy every second
            self.spawn_enemy()
            self.spawn_timer = 0

        # Update enemies
        for enemy in self.enemies[:]:
            enemy.y += self.enemy_speed
            if enemy.top > self.screen_height:
                self.enemies.remove(enemy)
                self.player_health -= 10  # Lose health if an enemy escapes

        # Check for collisions between bullets and enemies
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if bullet.colliderect(enemy):
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.xp += 20  # Gain XP for defeating an enemy
                    break

        # Level up if XP is sufficient
        if self.xp >= self.xp_to_next_level:
            self.level += 1
            self.xp -= self.xp_to_next_level
            self.xp_to_next_level += 50  # Increase XP requirement for next level

        # Check for game over
        if self.player_health <= 0:
            self.running = False

    def draw(self):
        """Render all game elements to the screen."""
        # Draw the background
        self.screen.blit(self.background, (0, 0))

        # Draw the player
        pygame.draw.rect(self.screen, self.player_color, self.player)

        # Draw bullets
        for bullet in self.bullets:
            pygame.draw.rect(self.screen, self.bullet_color, bullet)

        # Draw enemies
        for enemy in self.enemies:
            pygame.draw.rect(self.screen, self.enemy_color, enemy)

        # Draw health bar
        pygame.draw.rect(self.screen, (255, 0, 0), (10, 10, 200, 20))  # Red background
        pygame.draw.rect(self.screen, (0, 255, 0), (10, 10, 200 * (self.player_health / 100), 20))  # Green foreground

        # Draw XP bar
        pygame.draw.rect(self.screen, (0, 0, 0), (10, 40, 200, 20))  # Black background
        pygame.draw.rect(self.screen, (0, 0, 255), (10, 40, 200 * (self.xp / self.xp_to_next_level), 20))  # Blue foreground

        # Draw level text
        level_text = self.font_small.render(f"Level: {self.level}", True, (255, 255, 255))
        self.screen.blit(level_text, (10, 70))

        # Refresh the screen
        pygame.display.flip()

# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()
