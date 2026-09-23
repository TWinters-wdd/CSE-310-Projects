import arcade

window = arcade.Window(title="Arcade tutorials")
window.center_window()

class GameView(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        # ShapeElementList for batch drawing
        self.batch = arcade.shape_list.ShapeElementList()

        # Ellipses
        ellipse1 = arcade.shape_list.create_ellipse_filled(440, 360, 50, 50, arcade.color.ROSE)

        ellipse2 = arcade.shape_list.create_ellipse_outline(640, 360, 50, 80, arcade.color.RED)

        ellipse3 = arcade.shape_list.create_ellipse_filled_with_colors(840, 360, 50, 80, arcade.color.RED, arcade.color.BLUE, 45)

        # Triangle
        triangle = arcade.shape_list.create_polygon(((0, 0), (100, 0), (50, 100)), arcade.color.BLUE)

        # Rectangle
        rect = arcade.shape_list.create_rectangle_filled(100, 360, 100, 150, arcade.color.GREEN)

        self.batch.append(ellipse1)
        self.batch.append(ellipse2)
        self.batch.append(ellipse3)
        self.batch.append(triangle)
        self.batch.append(rect)

    def on_draw(self) -> None:
        self.clear()
        self.batch.draw()

game = GameView()
window.show_view(game)
arcade.run()
