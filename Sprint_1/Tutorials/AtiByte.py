import arcade

window = arcade.Window(title="Arcade tutorials")
window.center_window()


class GameView(arcade.View):
    def __init__(self) -> None:
        super().__init__()

    def on_draw(self) -> None:
        self.clear()

        # draw circles
        arcade.draw_circle_filled(100, 100, 30, (255, 0, 0))
        arcade.draw_circle_outline(150, 150, 30, (255, 0, 0))

        # draw rectangles
        arcade.draw_lbwh_rectangle_filled(250, 250, 100, 100, (100, 0, 100))

        arcade.draw_lbwh_rectangle_filled(200, 200, 100, 100, (0, 0, 255, 100))

        arcade.draw_lbwh_rectangle_outline(250, 50, 100, 100, (0, 0, 255))

        # draw arcs
        arcade.draw_arc_filled(500, 300, 100, 100, (0, 255, 0), 0, 90)
        arcade.draw_arc_outline(550, 350, 100, 100, (0, 255, 0), 0, 90)

        # draw a parabola
        arcade.draw_parabola_filled(250, 450, 300, 100, (255, 0, 255))

        # draw a line
        arcade.draw_line(600, 600, 800, 650, (0, 255, 255), 2)


game = GameView()
window.show_view(game)
arcade.run()
