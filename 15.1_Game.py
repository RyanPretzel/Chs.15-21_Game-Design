'''
SPRITE GAME
-----------
Here you will start the beginning of a game that you will be able to update as we
learn more in upcoming chapters. Below are some ideas that you could include:

1.) Find some new sprite images.
2.) Move the player sprite with arrow keys rather than the mouse. Don't let it move off the screen.
3.) Move the other sprites in some way like moving down the screen and then re-spawning above the window.
4.) Use sounds when a sprite is killed or the player hits the sidewall.
5.) See if you can reset the game after 30 seconds. Remember the on_update() method runs every 1/60th of a second.
6.) Try some other creative ideas to make your game awesome. Perhaps collecting good sprites while avoiding bad sprites.
7.) Keep score and use multiple levels. How do you keep track of an all time high score?
8.) Make a two player game.

'''

import random
import arcade
import math

# --- Constants ---
SW = 800
SH = 600
FIGHTER_SCALE = 0.3
ENEMY_PLANE_SCALE = 0.1
BULLET_SCALE = 1

# Movement Constants
ANGLE_SPEED = 4
MIN_PLANE_SPEED = 2
MAX_PLANE_SPEED = 5
BULLET_SPEED = 20
ENEMY_PLANE_SPEED = 2.5

EXPLOSION_TEXTURE_LIST = 50


# ------Fighter Jet/Player------------
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/fighter1.png", FIGHTER_SCALE)
        self.laser_sound = arcade.load_sound("sounds/laser.mp3")
        self.explosion_sound = arcade.load_sound("sounds/explosion.mp3")
        self.speed = 0
        self.change_angle = 0

    def update(self):
        self.angle += self.change_angle
        angle_rad = math.radians(self.angle)

        # trig to figure out distance change based on speed and angle
        self.center_x += -self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)
        # use if statements to keep bb8 in walls
        if self.left < 0:
            self.left = 0
        if self.right > SW:
            self.right = SW
        if self.top > SH:
            self.top = SH
        if self.bottom < 0:
            self.bottom = 0


# ---------Bullet/Laser-------------
class Bullet(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/bullet.png", BULLET_SCALE)

    def update(self):
        angle_shoot = math.radians(self.angle - 90)
        self.center_x += -self.speed * math.sin(angle_shoot)
        self.center_y += self.speed * math.cos(angle_shoot)
        if self.bottom > SH or self.top < 0 or self.right < 0 or self.left > SW:
            self.kill()


# -------Explosion---------
class Explosion(arcade.Sprite):
    def __init__(self, texture_list):
        super().__init__("Images/explosions/explosion0000.png")

        self.current_texture = 0
        self.textures = texture_list
        self.explosion_sound = arcade.load_sound("sounds/explosion.mp3")

    def update(self):
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.kill()


# ---------Enemy Plane------------
class EnemyPlane(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/enemy_plane.png", ENEMY_PLANE_SCALE)
        self.speed = ENEMY_PLANE_SPEED

    def update(self):
        angle_shoot = math.radians(self.angle - 45)
        self.center_x += -self.speed * math.sin(angle_shoot)
        self.center_y += self.speed * math.cos(angle_shoot)
        if self.bottom > SH or self.top < 0 or self.right < 0 or self.left > SW:
            self.kill()


# ------MyGame Class--------------
class MyGame(arcade.Window):
    def __init__(self, SW, SH, title):
        super().__init__(SW, SH, title)

        self.set_mouse_visible(False)

        self.current_state = 0
        self.game_running = False

        self.explosion_texture_list = []
        for i in range(EXPLOSION_TEXTURE_LIST):
            texture_name = f"Images/explosions/explosion{i:04}.png"
            self.explosion_texture_list.append(arcade.load_texture(texture_name))

    def setup(self):   # setup the game
        if self.current_state == 1:     # check which level is active and set variables accordingly
            arcade.set_background_color(arcade.color.SKY_BLUE)
            self.enemy_count = 1

        elif self.current_state == 2:
            arcade.set_background_color(arcade.color.BLUE_GRAY)
            self.enemy_count = 2

        elif self.current_state == 3:
            arcade.set_background_color(arcade.color.BLUE_GREEN)
            self.enemy_count = 3

        # sprite lists
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_plane_list = arcade.SpriteList()
        # enemy bullet list
        self.explosion_list = arcade.SpriteList()

        # create the player
        self.fighter = Player()
        self.fighter.center_x = SW / 2
        self.fighter.center_y = SH / 2
        self.fighter.speed = 2
        self.player_list.append(self.fighter)

        for i in range(self.enemy_count):
            eplane = EnemyPlane()
            # depending on which number the plane is in the list, it will determine the direction
            if i % 4 == 0:
                eplane.center_x = random.randrange(int(SW/3), int(SW * 2/3))
                eplane.center_y = 0     # from the bottom of the screen
                eplane.angle = random.randrange(5, 85)

            elif i % 4 == 1:
                eplane.center_x = random.randrange(int(SW/3), int(SW * 2/3))
                eplane.center_y = SH        # from the top
                eplane.angle = random.randrange(160, 280)

            elif i % 4 == 2:
                eplane.center_x = 0     # from the left
                eplane.center_y = random.randrange(int(SH/3), int(SH * 2/3))
                eplane.angle = random.randrange(-90, 0)

            else:           # from the right
                pass        # only used in a 4th level so its not done
            # eplane.angle = 0            # 0 deg is 45 deg in the picture
            self.enemy_plane_list.append(eplane)

    def on_draw(self):
        arcade.start_render()
        if self.current_state == 0:
            arcade.draw_rectangle_filled(SW // 2, SH // 2, SW, SH, arcade.color.BLACK)
            arcade.draw_text("Use W, A, S, and D to move the plane and use SPACE to shoot.  Choose level 1, 2, or 3.",
                             SW / 2 - 290, SH / 2, (0, 255, 0), 14)

        elif self.game_running is True:
            self.player_list.draw()
            self.bullet_list.draw()
            self.enemy_plane_list.draw()
            self.explosion_list.draw()

            arcade.draw_lrtb_rectangle_filled(SW - 95, SW, SH, SH - 55, arcade.color.WHITE)
            output = f"Level: {self.current_state}"
            arcade.draw_text(output, SW - 90, SH - 15, arcade.color.BLACK, 14)
            output = f"Score: {self.score}"
            arcade.draw_text(output, SW - 90, SH - 35, arcade.color.BLACK, 14)
            output = f"Speed: {self.fighter.speed}"
            arcade.draw_text(output, SW - 90, SH - 55, arcade.color.BLACK, 14)

        else:       # draw game over screen
            output = f"Score: {self.score}"
            arcade.draw_rectangle_filled(SW // 2, SH // 2, SW, SH, arcade.color.BLACK)
            arcade.draw_text("Game over! Choose level 1, 2, or 3 to play again!", SW / 2 - 150, SH / 2, (0, 255, 0), 14)
            arcade.draw_text("Press I for instructions.", SW / 2 - 90, SH / 2 - 20, (0, 255, 0), 14)
            arcade.draw_text(output, SW / 2 - 35, SH / 2 - 40, arcade.color.WHITE, 14)

    def on_update(self, dt):
        if self.current_state > 0 and self.current_state < 4:
            self.game_running = True

        else:
            self.game_running = False

        if self.game_running is True:
            self.player_list.update()
            self.bullet_list.update()
            self.explosion_list.update()
            self.enemy_plane_list.update()

            if len(self.enemy_plane_list) == 0:
                self.current_state += 1
                self.setup()

            self.plane_hit = arcade.check_for_collision_with_list(self.fighter, self.enemy_plane_list)
            # check if fighter is colliding with another plane
            if len(self.plane_hit) > 0:
                self.fighter.kill()
                self.current_state = 4

            for bullet in self.bullet_list:
                # check if a bullet and trooper are colliding
                hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_plane_list)

                # create the explosion
                if len(hit_list) > 0:
                    explosion = Explosion(self.explosion_texture_list)
                    explosion.center_x = hit_list[0].center_x
                    explosion.center_y = hit_list[0].center_y
                    self.explosion_list.append(explosion)
                    arcade.play_sound(explosion.explosion_sound)

                for eplane in hit_list:
                    eplane.kill()
                    self.score += 1

    def on_key_press(self, key, modifiers: int):
        if key == arcade.key.A and self.game_running:
            self.fighter.change_angle = ANGLE_SPEED

        elif key == arcade.key.D and self.game_running:
            self.fighter.change_angle = -ANGLE_SPEED

        elif key == arcade.key.W and self.game_running and self.fighter.speed < MAX_PLANE_SPEED:
            self.fighter.speed += 1

        elif key == arcade.key.S and self.game_running and self.fighter.speed > MIN_PLANE_SPEED:
            self.fighter.speed -= 1

        elif key == arcade.key.SPACE and self.game_running:
            self.bullet = Bullet()
            self.bullet.center_x = self.fighter.center_x
            self.bullet.center_y = self.fighter.center_y
            self.bullet.angle = self.fighter.angle + 90
            self.bullet.speed = BULLET_SPEED
            self.bullet_list.append(self.bullet)
            arcade.play_sound(self.fighter.laser_sound)

        # level selector
        elif key == arcade.key.I and not self.game_running:
            self.current_state = 0
        elif key == arcade.key.KEY_1 and not self.game_running:
            self.current_state = 1
            self.score = 0
            self.setup()
        elif key == arcade.key.KEY_2 and not self.game_running:
            self.current_state = 2
            self.score = 0
            self.setup()
        elif key == arcade.key.KEY_3 and not self.game_running:
            self.current_state = 3
            self.score = 0
            self.setup()

    def on_key_release(self, key, modifiers: int):
        if (key == arcade.key.A or key == arcade.key.D) and self.game_running is True:
            self.fighter.change_angle = 0


# -----Main Function--------
def main():
    window = MyGame(SW, SH, "Fighter go brrrr")
    arcade.run()


# ------Run Main Function-----
if __name__ == "__main__":
    main()
