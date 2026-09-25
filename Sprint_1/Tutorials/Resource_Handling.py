import arcade
from pathlib import Path # Allows for distribution of assets, instead of typing a full on path, you can use Path(__file__).parent.resolve() / Path("images") to simplify the absolute path

window = arcade.Window(title="Resource Handling Tutorial")
window.center_window()

# assets_path = Path(__file__).parent.resolve() / Path("images")
assets_path = Path().absolute() / Path("images")

# How to add your own resources to the sprite list (The path must be absolute)
arcade.resources.add_resource_handle("my-images", assets_path)



class GameView(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        img1 = ":resources:images/animated_characters/female_person/femalePerson_idle.png"
        self.player_sprite = arcade.Sprite(img1, scale=1)
        self.player_sprite.position = 240, 360

        img2 = ":resources:/images/alien/alienBlue_front.png"
        self.alien_sprite = arcade.Sprite(img2, scale=1)
        self.alien_sprite.position = 440, 360

        logo = ":resources:/logo.png"
        self.logo_sprite = arcade.Sprite(logo, scale=0.2)
        self.logo_sprite.position = 640, 360

        img3 = ":my-images:mounted-knight.png"
        self.knight_sprite = arcade.Sprite(img3, scale=0.2)
        self.knight_sprite.position = 840, 360

        # SpriteList for batch drawing the Sprites
        self.sprite_list = arcade.SpriteList()
        self.sprite_list.append(self.player_sprite)
        self.sprite_list.append(self.alien_sprite)
        self.sprite_list.append(self.logo_sprite)
        self.sprite_list.append(self.knight_sprite)


    def on_draw(self) -> None:
        self.clear()
        self.sprite_list.draw()


game = GameView()
window.show_view(game)
arcade.run()