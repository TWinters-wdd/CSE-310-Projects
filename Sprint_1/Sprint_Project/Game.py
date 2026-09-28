"""A small, asset-free Python Arcade game.

The player stands in one place while the background scrolls from right to
left. Enemies approach in straight lines from the left, top, and right. Use the
matching key to attack:

    W = attack an enemy coming from above
    A = attack an enemy coming from the left
    D = attack an enemy coming from the right

The colored rectangles are Arcade sprites. They are intentionally simple so
that they can be replaced with image files later without changing the game
logic.
"""

from __future__ import annotations

import random
from pathlib import Path
from typing import Optional

import arcade


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Auto Runner: Three-Way Attack"

PLAYER_Y = 125
BACKGROUND_SPEED = 160
ENEMY_SPEED = 100
SPAWN_INTERVAL = 1.15
HERO_SCALE = 2.2
HERO_FRAME_SIZE = 64
HERO_ATTACK_TIME = 0.42

HERO_SPRITE_DIR = (
    Path(__file__).resolve().parent
    / "Images"
    / "PNG"
    / "Swordsman_lvl3"
    / "With_shadow"
)


class Enemy(arcade.SpriteSolidColor):
    """A simple enemy that remembers which attack can defeat it."""

    def __init__(self, side: str) -> None:
        colors = {
            "left": arcade.color.ORANGE_RED,
            "top": arcade.color.PURPLE,
            "right": arcade.color.DARK_ORANGE,
        }
        super().__init__(34, 34, colors[side])
        self.side = side
        self.speed = ENEMY_SPEED + random.randint(-15, 25)


class HeroPlayer(arcade.Sprite):
    """Animated level 3 swordsman used for the stationary player."""

    # The PNG sprite sheets contain four 64-pixel rows. In the level 3 sheets
    # the rows are front, left, right, and back, respectively. These rows give
    # the player a matching view for each attack direction.
    DIRECTION_ROWS = {
        "left": 1,
        "right": 2,
        "top": 3,
    }

    SHEETS = {
        "run": "Swordsman_lvl3_Run_with_shadow.png",
        "attack": "Swordsman_lvl3_attack_with_shadow.png",
        "hurt": "Swordsman_lvl3_Hurt_with_shadow.png",
    }

    def __init__(self) -> None:
        animation_indices: dict[str, dict[str, list[int]]] = {}
        all_textures = []

        for animation_name, file_name in self.SHEETS.items():
            sheet_path = HERO_SPRITE_DIR / file_name
            sheet = arcade.load_spritesheet(sheet_path)
            sheet_width, sheet_height = sheet.image.size
            columns = sheet_width // HERO_FRAME_SIZE
            rows = sheet_height // HERO_FRAME_SIZE
            sheet_textures = sheet.get_texture_grid(
                (HERO_FRAME_SIZE, HERO_FRAME_SIZE),
                columns,
                columns * rows,
            )

            animation_indices[animation_name] = {}
            for direction, row in self.DIRECTION_ROWS.items():
                first_frame = row * columns
                frames = sheet_textures[first_frame : first_frame + columns]
                animation_indices[animation_name][direction] = []
                for texture in frames:
                    animation_indices[animation_name][direction].append(
                        len(all_textures)
                    )
                    all_textures.append(texture)

        super().__init__(all_textures[0], scale=HERO_SCALE)
        for texture in all_textures[1:]:
            self.append_texture(texture)

        self.animation_indices = animation_indices
        self.state = "run"
        self.direction = "right"
        self.animation_time = 0.0

    def start_attack(self, direction: str) -> None:
        """Start a one-shot attack animation in the requested direction."""
        self.direction = direction
        self.state = "attack"
        self.animation_time = 0.0

    def start_hurt(self) -> None:
        """Play the damage-taken animation, then return to running."""
        self.state = "hurt"
        self.animation_time = 0.0

    def update_animation(self, delta_time: float) -> None:
        self.animation_time += delta_time

        if self.state == "attack" and self.animation_time >= HERO_ATTACK_TIME:
            self.state = "run"
            self.animation_time = 0.0
        elif self.state == "hurt" and self.animation_time >= 0.35:
            self.state = "run"
            self.animation_time = 0.0

        frame_time = {
            "run": 0.09,
            "attack": HERO_ATTACK_TIME / 8,
            "hurt": 0.08,
        }[self.state]
        frames = self.animation_indices[self.state][self.direction]
        frame_number = int(self.animation_time / frame_time)
        if self.state == "run":
            frame_number %= len(frames)
        else:
            frame_number = min(frame_number, len(frames) - 1)
        self.set_texture(frames[frame_number])


class GameView(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        self.player: HeroPlayer
        self.player_list = arcade.SpriteList()
        self.enemies = arcade.SpriteList()
        self.sun: arcade.SpriteCircle
        self.sun_list = arcade.SpriteList()

        self.score = 0
        self.lives = 3
        self.spawn_timer = 0.0
        self.background_scroll = 0.0
        self.attack_direction: Optional[str] = None
        self.attack_timer = 0.0
        self.game_over = False

        # Arcade includes this sound in its built-in resources. If a very
        # old Arcade installation does not include it, the game still runs.
        self.kill_sound = None
        try:
            self.kill_sound = arcade.Sound(":resources:sounds/hit1.wav")
        except (FileNotFoundError, OSError, AttributeError):
            pass

        self.setup()

    def setup(self) -> None:
        """Create the animated player, fixed sun, and enemy list."""
        self.enemies = arcade.SpriteList()
        self.sun_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

        self.player = HeroPlayer()
        self.player.center_x = SCREEN_WIDTH / 2
        self.player.center_y = PLAYER_Y
        self.player_list.append(self.player)

        # The sun is the game's unmovable object. It stays at a fixed screen
        # position while the rest of the background scrolls behind it.
        self.sun = arcade.SpriteCircle(58, arcade.color.GOLD)
        self.sun.center_x = 820
        self.sun.center_y = 585
        self.sun_list.append(self.sun)

        self.score = 0
        self.lives = 3
        self.spawn_timer = 0.0
        self.background_scroll = 0.0
        self.attack_direction = None
        self.attack_timer = 0.0
        self.game_over = False

    def spawn_enemy(self) -> None:
        side = random.choice(("left", "top", "right"))
        enemy = Enemy(side)

        if side == "left":
            enemy.center_x = -30
            # Left enemies stay directly level with the player.
            enemy.center_y = self.player.center_y
        elif side == "right":
            enemy.center_x = SCREEN_WIDTH + 30
            # Right enemies stay directly level with the player.
            enemy.center_y = self.player.center_y
        else:
            # Top enemies stay directly above the player.
            enemy.center_x = self.player.center_x
            enemy.center_y = SCREEN_HEIGHT + 30

        self.enemies.append(enemy)

    def on_draw(self) -> None:
        self.clear()

        # The sky stays in place while the scenery scrolls from right to left.
        arcade.draw_lbwh_rectangle_filled(
            0,
            0,
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            arcade.color.ROYAL_BLUE,
        )

        self.draw_scrolling_background()
        # Draw the unmovable sun before the clouds so clouds can pass over it.
        self.sun_list.draw()
        self.draw_scrolling_clouds()
        arcade.draw_lbwh_rectangle_filled(
            0,
            0,
            SCREEN_WIDTH,
            150,
            arcade.color.DARK_SPRING_GREEN,
        )
        arcade.draw_line(0, 150, SCREEN_WIDTH, 150, arcade.color.LIGHT_GREEN, 4)

        self.enemies.draw()
        self.player_list.draw()

        # Draw a short attack indicator while an attack is active.
        if self.attack_timer > 0 and self.attack_direction:
            left, bottom, width, height = self.get_attack_box()
            arcade.draw_lbwh_rectangle_outline(
                left,
                bottom,
                width,
                height,
                arcade.color.YELLOW,
                4,
            )

        arcade.draw_text(
            f"Score: {self.score}    Lives: {self.lives}",
            20,
            SCREEN_HEIGHT - 42,
            arcade.color.WHITE,
            20,
        )
        arcade.draw_text(
            "W: top attack     A: left attack     D: right attack",
            20,
            20,
            arcade.color.WHITE,
            16,
        )

        if self.game_over:
            arcade.draw_lbwh_rectangle_filled(
                (SCREEN_WIDTH - 540) / 2,
                (SCREEN_HEIGHT - 190) / 2,
                540,
                190,
                (20, 20, 35, 235),
            )
            arcade.draw_text(
                "GAME OVER",
                SCREEN_WIDTH / 2,
                390,
                arcade.color.WHITE,
                34,
                anchor_x="center",
            )
            arcade.draw_text(
                "Press R to run again",
                SCREEN_WIDTH / 2,
                345,
                arcade.color.YELLOW,
                20,
                anchor_x="center",
            )

    def get_attack_box(self) -> tuple[float, float, float, float]:
        """Return (left, bottom, width, height) for the current attack."""
        if self.attack_direction == "top":
            return self.player.center_x - 36, self.player.top, 72, 82
        if self.attack_direction == "left":
            return self.player.left - 82, self.player.center_y - 36, 82, 72
        return self.player.right, self.player.center_y - 36, 82, 72

    def attack(self, direction: str) -> None:
        self.attack_direction = direction
        self.attack_timer = HERO_ATTACK_TIME
        self.player.start_attack(direction)

    def check_attack_collisions(self) -> None:
        if not self.attack_direction or self.attack_timer <= 0:
            return

        left, bottom, width, height = self.get_attack_box()
        attack_box = arcade.SpriteSolidColor(width, height, arcade.color.WHITE)
        attack_box.center_x = left + width / 2
        attack_box.center_y = bottom + height / 2

        for enemy in list(self.enemies):
            # The matching key is required for each approach direction.
            if enemy.side != self.attack_direction:
                continue
            if arcade.check_for_collision(attack_box, enemy):
                enemy.remove_from_sprite_lists()
                self.score += 1
                if self.kill_sound is not None:
                    arcade.play_sound(self.kill_sound)

    def on_update(self, delta_time: float) -> None:
        self.player.update_animation(delta_time)

        if self.game_over:
            return

        # Move the scenery left while keeping the player at the same screen
        # position. This creates the illusion that the player is running.
        self.background_scroll = (
            self.background_scroll - BACKGROUND_SPEED * delta_time
        ) % SCREEN_WIDTH
        self.spawn_timer += delta_time
        self.attack_timer = max(0.0, self.attack_timer - delta_time)

        if self.spawn_timer >= SPAWN_INTERVAL:
            self.spawn_timer = 0.0
            self.spawn_enemy()

        # Enemies attack on one straight lane only. They never travel
        # diagonally, so each key clearly matches one approach direction.
        for enemy in self.enemies:
            if enemy.side == "left":
                enemy.center_y = self.player.center_y
                enemy.center_x += enemy.speed * delta_time
            elif enemy.side == "right":
                enemy.center_y = self.player.center_y
                enemy.center_x -= enemy.speed * delta_time
            else:  # top
                enemy.center_x = self.player.center_x
                enemy.center_y -= enemy.speed * delta_time

        self.check_attack_collisions()

        # Collision between the player and each moving enemy.
        for enemy in list(self.enemies):
            if arcade.check_for_collision(self.player, enemy):
                enemy.remove_from_sprite_lists()
                self.lives -= 1
                self.attack_direction = None
                self.attack_timer = 0.0
                self.player.start_hurt()
                if self.lives <= 0:
                    self.game_over = True

        # Remove enemies that have drifted far off-screen.
        for enemy in list(self.enemies):
            if (
                enemy.right < -120
                or enemy.left > SCREEN_WIDTH + 120
                or enemy.top < -120
            ):
                enemy.remove_from_sprite_lists()

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key == arcade.key.R and self.game_over:
            self.setup()
        elif not self.game_over and key == arcade.key.W:
            self.attack("top")
        elif not self.game_over and key == arcade.key.A:
            self.attack("left")
        elif not self.game_over and key == arcade.key.D:
            self.attack("right")

    def draw_scrolling_background(self) -> None:
        """Draw repeating hills and ground markings behind the fixed sun."""
        offset = self.background_scroll

        # Repeating hills are drawn three times so they wrap smoothly.
        for x in (0, 310, 620, 930):
            for wrapped_x in (x + offset - SCREEN_WIDTH, x + offset, x + offset + SCREEN_WIDTH):
                arcade.draw_triangle_filled(
                    wrapped_x - 230,
                    175,
                    wrapped_x,
                    390,
                    wrapped_x + 230,
                    175,
                    arcade.color.DARK_SPRING_GREEN,
                )

        for x in (150, 500, 850):
            for wrapped_x in (x + offset - SCREEN_WIDTH, x + offset, x + offset + SCREEN_WIDTH):
                arcade.draw_triangle_filled(
                    wrapped_x - 250,
                    175,
                    wrapped_x,
                    330,
                    wrapped_x + 250,
                    175,
                    arcade.color.FOREST_GREEN,
                )

        # These lane marks provide a clear visual cue that the world is moving.
        for x in range(-80, SCREEN_WIDTH + 80, 80):
            shifted_x = x + offset
            arcade.draw_line(
                shifted_x,
                92,
                shifted_x + 36,
                92,
                arcade.color.LIGHT_GREEN,
                3,
            )

    def draw_scrolling_clouds(self) -> None:
        """Draw clouds that move over the fixed sun."""
        offset = self.background_scroll
        for cloud_x, cloud_y in ((180, 555), (590, 500), (980, 610)):
            for wrapped_x in (
                cloud_x + offset - SCREEN_WIDTH,
                cloud_x + offset,
                cloud_x + offset + SCREEN_WIDTH,
            ):
                arcade.draw_circle_filled(wrapped_x, cloud_y, 24, arcade.color.WHITE)
                arcade.draw_circle_filled(wrapped_x + 28, cloud_y + 4, 30, arcade.color.WHITE)
                arcade.draw_circle_filled(wrapped_x + 58, cloud_y, 21, arcade.color.WHITE)

def main() -> None:
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.show_view(GameView())
    arcade.run()


if __name__ == "__main__":
    main()
