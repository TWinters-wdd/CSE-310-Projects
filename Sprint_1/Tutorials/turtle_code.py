import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SPEED = 5

# class MyGame(arcade.Window):
#     """Basic window example."""

#     def __init__(self):
#         super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Hello Window")

#     def on_draw(self):
#         """Render the screen."""
#         self.clear()
#         arcade.draw_text("Hello Arcade!", 300, 300, arcade.color.WHITE, 20)


# class MyGame(arcade.Window):
#     """Sprite example."""

#     def __init__(self):
#         super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Sprite Example")

#         # SpriteList to manage all sprites
#         self.all_sprites = arcade.SpriteList()

#         # Create a red square sprite
#         texture = arcade.make_soft_square_texture(50, arcade.color.RED, 255, 255)
#         self.player = arcade.Sprite(center_x=400, center_y=300)
#         self.player.append_texture(texture)
#         self.player.set_texture(0)
#         self.all_sprites.append(self.player)

#         # Movement flags
#         self.up = self.down = self.left = self.right = False


#     def on_draw(self):
#         """Render the screen."""
#         self.clear()
#         self.all_sprites.draw()

#     def on_update(self, delta_time):
#         """Update sprite position based on key presses."""
#         if self.up:
#             self.player.center_y += SPEED
#         if self.down:
#             self.player.center_y -= SPEED
#         if self.left:
#             self.player.center_x -= SPEED
#         if self.right:
#             self.player.center_x += SPEED

#     def on_key_press(self, key, modifiers):
#         """Set movement flags on key press."""
#         if key == arcade.key.UP:
#             self.up = True
#         elif key == arcade.key.DOWN:
#             self.down = True
#         elif key == arcade.key.LEFT:
#             self.left = True
#         elif key == arcade.key.RIGHT:
#             self.right = True

#     def on_key_release(self, key, modifiers):
#         """Reset movement flags on key release."""
#         if key == arcade.key.UP:
#             self.up = False
#         elif key == arcade.key.DOWN:
#             self.down = False
#         elif key == arcade.key.LEFT:
#             self.left = False
#         elif key == arcade.key.RIGHT:
#             self.right = False

# COLLISION EXAMPLE
class MyGame(arcade.Window):
    """Collision example with mouse-controlled player."""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Collision Example")

        # Sprite Lists
        self.all_sprites = arcade.SpriteList()   # For drawing
        self.enemies = arcade.SpriteList()       # For collision

        # Player sprite
        player_texture = arcade.make_soft_square_texture(40, arcade.color.BLUE, 255, 255)
        self.player = arcade.Sprite(center_x=400, center_y=300)
        self.player.append_texture(player_texture)
        self.player.set_texture(0)
        self.all_sprites.append(self.player)

        # Create enemy sprites
        for _ in range(5):
            enemy_texture = arcade.make_soft_square_texture(30, arcade.color.RED, 255, 255)

            enemy = arcade.Sprite(center_x=random.randint(50, SCREEN_WIDTH - 50), center_y=random.randint(50, SCREEN_HEIGHT - 50))
            enemy.append_texture(enemy_texture)
            enemy.set_texture(0)
            self.enemies.append(enemy)

        # Add enemies to main sprite list for drawing
        self.all_sprites.extend(self.enemies)

        # Track mouse position
        self.mouse_x = self.player.center_x
        self.mouse_y = self.player.center_y

    def on_draw(self):
        """Render the screen."""
        self.clear()
        self.all_sprites.draw()

    def on_update(self, delta_time):
        """Update player position and check collisions."""
        # Move player to follow mouse
        self.player.center_x = self.mouse_x
        self.player.center_y = self.mouse_y

        # Check for collisions with enemies
        hit_list = arcade.check_for_collision_with_list(self.player, self.enemies)
        for enemy in hit_list:
            # Change enemy color on collision
            enemy.color = arcade.color.GREEN

    def on_mouse_motion(self, x, y, dx, dy):
        """Update mouse position."""
        self.mouse_x = x
        self.mouse_y = y

if __name__ == "__main__":
    game = MyGame()
    arcade.run()