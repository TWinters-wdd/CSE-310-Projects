import arcade

window = arcade.Window(title="Arcade tutorials")
window.center_window()


class GameView(arcade.View):
    def __init__(self) -> None:
        super().__init__()
        self.circle_x = 640
        self.circle_y = 360
        self.speed_x = 500
        self.speed_y = 500
        self.radius = 40

    def on_draw(self) -> None:
        self.clear()
        arcade.draw_circle_filled(self.circle_x, self.circle_y, self.radius, arcade.color.AO)

        arcade.draw_circle_outline(self.circle_x, self.circle_y, self.radius, arcade.color.YELLOW, 2)

        # draw_text is slow, use this function only for testing
        arcade.draw_text(f"x: {self.circle_x:.2f} - y: {self.circle_y:.2f}", 10, 700, arcade.color.WHITE, 20)

    def on_update(self, delta_time: float) -> None:
        self.circle_x += self.speed_x * delta_time
        self.circle_y += self.speed_y * delta_time
        # Right side of the windown
        if self.circle_x > self.width - self.radius:
            self.circle_x = self.width - self.radius
            self.speed_x *= -1

        # Left side of the window
        if self.circle_x < self.radius:
            self.circle_x = self.radius
            self.speed_x *= -1

        # Top of the window
        if self.circle_y > self.height - self.radius:
            self.circle_y = self.height - self.radius
            self.speed_y *= -1

        # Bottom of the window
        if self.circle_y < self.radius:
            self.circle_y = self.radius
            self.speed_y *= -1

game = GameView()
window.show_view(game)
arcade.run()