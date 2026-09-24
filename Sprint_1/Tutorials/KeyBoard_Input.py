import arcade

window = arcade.Window(title="Key Board Input Tutorial")
window. center_window()


class GameView(arcade.View):
    def __init__(self) -> None:
        super().__init__()
        self.circle_x = 640
        self.circle_y = 360
        self.circle_speed = 500
        self.directions = {'left': False, 'right': False, 'up': False, 'down': False}


    def on_draw(self) -> None:
        self.clear()
        arcade.draw_ellipse_filled(self.circle_x, self.circle_y, 80, 80, arcade.color.AO)
        arcade.draw_ellipse_outline(self.circle_x, self.circle_y, 80, 80, arcade.color.YELLOW, 2)

        # draw_text is slow, use this function only for testing
        arcade.draw_text(f"x: {self.circle_x:.2f} - y: {self.circle_y:.2f}", 10, 700, arcade.color.WHITE, 20)

    def on_key_press(self, symbol, modifiers) -> None:
        if symbol == arcade.key.LEFT:
            self.directions['left'] = True
        if symbol == arcade.key.RIGHT:
            self.directions['right'] = True
        if symbol == arcade.key.UP:
            self.directions['up'] = True
        if symbol == arcade.key.DOWN:
            self.directions['down'] = True

        # Combination of keys
        if modifiers & arcade.key.MOD_SHIFT and symbol == arcade.key.C:
            print("Shift+C")

    def on_key_release(self, symbol, modifiers) -> None:
        if symbol == arcade.key.LEFT:
            self.directions['left'] = False
        if symbol == arcade.key.RIGHT:
            self.directions['right'] = False
        if symbol == arcade.key.UP:
            self.directions['up'] = False
        if symbol == arcade.key.DOWN:
            self.directions['down'] = False

    def on_update(self, delta_time) -> None:
        if self.directions['left']:
            self.circle_x -= self.circle_speed * delta_time
        if self.directions['right']:
            self.circle_x += self.circle_speed * delta_time
        if self.directions['up']:
            self.circle_y += self.circle_speed * delta_time
        if self.directions['down']:
            self.circle_y -= self.circle_speed * delta_time


game = GameView()
window.show_view(game)
arcade.run()