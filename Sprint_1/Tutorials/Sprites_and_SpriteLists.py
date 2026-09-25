import arcade

window = arcade.Window(title="Sprites and SpriteLists")
window.center_window()


class GameView(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        img1 = "images/diplodocus.png"
        self.dino_sprite = arcade.Sprite(img1, scale=0.25)
        self.dino_sprite.position = 440, 360

        img2 = "images/mounted-knight.png"
        self.knight_sprite = arcade.Sprite(img2, scale=0.25)
        self.knight_sprite.position = 640, 360

        # SpriteList for batch drawing Sprites
        self.sprite_list = arcade.SpriteList()
        self.sprite_list.append(self.dino_sprite)
        self.sprite_list.append(self.knight_sprite)


    def on_draw(self) -> None:
        self.clear()
        self.sprite_list.draw()

    def on_update(self, delta_time) -> None:
        self.knight_sprite.angle += 1


game = GameView()
window.show_view(game)
arcade.run()