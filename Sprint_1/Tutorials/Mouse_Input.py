import arcade

window = arcade.Window(title="Mouse Input Tutorial")
window.center_window()
window.set_mouse_visible(False)


class GameView(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        self.green_circle_x = 640
        self.green_circle_y = 360

        self.blue_circle_x = 100
        self.blue_circle_y = 250

        self.red_circle_x = 350
        self.red_circle_y = 150

    def on_draw(self) -> None:
        self.clear()

        # Green circle
        arcade.draw_ellipse_filled(self.green_circle_x, self.green_circle_y, 80, 80, arcade.color.GREEN)

        # Blue circle
        arcade.draw_ellipse_filled(self.blue_circle_x, self.blue_circle_y, 80, 80, arcade.color.BLUE)

        # Red circle
        arcade.draw_ellipse_outline(self.red_circle_x, self.red_circle_y, 80, 80, arcade.color.RED, 2)

    def on_mouse_press(self, x, y, button, modifiers) -> None:
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.green_circle_x = x
            self.green_circle_y = y
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.blue_circle_x = x
            self.blue_circle_y = y

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        self.red_circle_x = x
        self.red_circle_y = y

game = GameView()
window.show_view(game)
arcade.run()