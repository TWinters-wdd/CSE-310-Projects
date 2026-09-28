import arcade

window = arcade.Window(title="Sprite Sheet Animations Tutorial")
window.center_window()

# TO DO: Find a spritesheet I can follow along with this tutorial

class GameView(arcade.View):
    def __init__(self) -> None:
        super().__init__()

    def on_draw(self) -> None:
        self.clear()


game = GameView()
window.show_view(game)
arcade.run()