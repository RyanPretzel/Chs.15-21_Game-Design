#Sign your name:________________
 
#You will use the starting code below and build the program "BB8 Attack" as you go through Chapter 15.


import random
import arcade

# --- Constants ---
BB8_scale = 0.3
trooper_scale = 0.1
trooper_count = 40
bullet_scale = 1
SW = 800
SH = 600
speed = 4


# -------Player/BB8--------
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/bb8.png", BB8_scale)

    def update(self):
        self.center_x += self.change_x
        if self.right < 0:
            self.right = SW
        elif self.left > SW:
            self.left = 0


# --------Trooper----------
class Trooper(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/stormtrooper.png", trooper_scale)
        self.w = int(self.width)
        self.h = int(self.height)

    def update(self):
        self.center_y -= 2
        if self.top < 0:
            self.center_x = random.randrange(self.w, SW - self.w)
            self.center_y = random.randrange(SH + self.h, SH * 2)


# -------Bullet-----------
class Bullet(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/bullet.png", bullet_scale)

    def update(self):
        self.center_y += 10
        if self.bottom > SH:
            self.kill()


# ------MyGame Class--------------
class MyGame(arcade.Window):
    def __init__(self, SW, SH, title):
        super().__init__(SW, SH, title)
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.set_mouse_visible(False)

    def reset(self):   # reset the game
        self.gameover = False

        # sprite lists
        self.player_list = arcade.SpriteList()
        self.trooper_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        self.score = 0

        # create the player
        self.BB8 = Player()
        self.BB8.center_x = SW/2
        self.BB8.bottom = 2
        self.player_list.append(self.BB8)

        # create the troopers
        for i in range(trooper_count):
            trooper = Trooper()
            trooper.center_x = random.randrange(trooper.w, SW - trooper.w)
            trooper.center_y = random.randrange(SH / 2, SH * 2)
            self.trooper_list.append(trooper)

    def on_draw(self):
        arcade.start_render()
        self.trooper_list.draw()
        self.player_list.draw()
        self.bullet_list.draw()

        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.BLACK, 14)

        if self.gameover is True:
            arcade.draw_rectangle_filled(SW // 2, SH // 2, SW, SH, arcade.color.BLACK)
            arcade.draw_text("Game over! Press 'P' to play again!", SW / 2 - 150, SH / 2, arcade.color.WHITE, 14)
            arcade.draw_text(output, SW / 2 - 50, SH / 2 - 20, arcade.color.WHITE, 14)

    def on_key_press(self, key, modifiers: int):
        if key == arcade.key.LEFT:
            self.BB8.change_x -= speed
        elif key == arcade.key.RIGHT:
            self.BB8.change_x += speed
        elif key == arcade.key.P:
            self.reset()
        elif key == arcade.key.SPACE and self.gameover is False:
            self.bullet = Bullet()
            self.bullet.center_x = self.BB8.center_x
            self.bullet.bottom = self.BB8.top
            self.bullet.angle = 90
            self.bullet_list.append(self.bullet)
            self.score -= 1

    def on_key_release(self, key, modifiers: int):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.BB8.change_x = 0

    def on_update(self, dt):
        self.player_list.update()
        self.trooper_list.update()
        self.bullet_list.update()

        if len(self.trooper_list) == 0:
            self.gameover = True

        self.bb8_hit = arcade.check_for_collision_with_list(self.BB8, self.trooper_list)
        # check if bb8 is colliding with a trooper
        if len(self.bb8_hit) > 0:
            self.BB8.kill()
            self.gameover = True

        for bullet in self.bullet_list:
            # check if a bullet and trooper are colliding
            hit_list = arcade.check_for_collision_with_list(bullet, self.trooper_list)

            if len(hit_list) > 0:
                bullet.kill()

            for trooper in hit_list:
                trooper.kill()
                self.score += 2


# -----Main Function--------
def main():
    window = MyGame(SW, SH, "BB8 Attack")
    window.reset()
    arcade.run()


# ------Run Main Function-----
if __name__ == "__main__":
    main()
