import arcade

window = arcade.Window(title="Week 1 Sprint Game")
window.center_window()


class GameView(arcade.View):
    def __init__(self) -> None:
        super().__init__()



game = GameView()
window.show_view(game)
arcade.run()