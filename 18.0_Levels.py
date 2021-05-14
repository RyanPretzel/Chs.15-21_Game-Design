

import random
import arcade
import math

# --- Constants ---
BB8_scale = 0.3
trooper_scale = 0.1
bullet_scale = 1
SW = 800
SH = 600
speed = 4
Bullet_Points = -1
Trooper_Points = 5

explosion_texture_count = 50

# game states
Instructions = 0
Level_1 = 1
Level_2 = 2
Level_3 = 3
Finished = 4

# speed constants
Movement_Speed = 5
Angle_Speed = 5
Bullet_Speed = 10
E_Bullet_Speed = 8


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


# -------Player/BB8--------
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/bb8.png", BB8_scale)
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


# --------Enemy Bullet-----
class EnemyBullet(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/rbullet.png", bullet_scale)
        self.angle_list = [0, 90, 180, 270]
        self.angle = random.choice(self.angle_list)

    def update(self):
        angle_shoot = math.radians(self.angle - 90)
        self.center_x += -E_Bullet_Speed * math.sin(angle_shoot)
        self.center_y += E_Bullet_Speed * math.cos(angle_shoot)
        if self.bottom > SH or self.top < 0 or self.right < 0 or self.left > SW:
            self.kill()


# --------Trooper----------
class Trooper(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/stormtrooper.png", trooper_scale)
        self.w = int(self.width)
        self.h = int(self.height)
        self.dx = random.randrange(-1, 2, 2)
        self.dy = random.randrange(-1, 2, 2)

    def update(self):
        self.center_x += self.dx
        self.center_y += self.dy
        if self.bottom < 0 or self.top > SH:
            self.dy *= -1
        elif self.left < 0 or self.right > SW:
            self.dx *= -1


# -------Bullet-----------
class Bullet(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/bullet.png", bullet_scale)

    def update(self):
        angle_shoot = math.radians(self.angle - 90)
        self.center_x += -self.speed * math.sin(angle_shoot)
        self.center_y += self.speed * math.cos(angle_shoot)
        if self.bottom > SH or self.top < 0 or self.right < 0 or self.left > SW:
            self.kill()


# ------MyGame Class--------------
class MyGame(arcade.Window):
    def __init__(self, SW, SH, title):
        super().__init__(SW, SH, title)
        # set game state
        self.current_state = 0
        self.game_running = False

        self.set_mouse_visible(False)

        self.explosion_texture_list = []
        for i in range (explosion_texture_count):
            texture_name = f"Images/explosions/explosion{i:04}.png"
            self.explosion_texture_list.append(arcade.load_texture(texture_name))

    def setup(self):   # setup the game
        if self.current_state == 1:     # check which level is active and set variables accordingly
            arcade.set_background_color(arcade.color.SKY_BLUE)
            self.background = arcade.load_texture("Images/sky1.png")
            self.trooper_count = 1

        elif self.current_state == 2:
            arcade.set_background_color(arcade.color.WHITE_SMOKE)
            self.background = arcade.load_texture("Images/sky2.png")
            self.trooper_count = 2

        elif self.current_state == 3:
            arcade.set_background_color(arcade.color.ROSE_RED)
            self.background = arcade.load_texture("Images/sky3.png")
            self.trooper_count = 3

        # sprite lists
        self.player_list = arcade.SpriteList()
        self.trooper_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.explosions = arcade.SpriteList()
        self.ebullets = arcade.SpriteList()

        # create the player
        self.BB8 = Player()
        self.BB8.center_x = SW/2
        self.BB8.center_y = SH/2
        self.player_list.append(self.BB8)

        # create the troopers
        for i in range(self.trooper_count):
            trooper = Trooper()
            if i % 2 == 0:
                trooper.center_x = random.randrange(trooper.w, int(SW / 3))
            else:
                trooper.center_x = random.randrange(int(SW * 2 / 3), SW - trooper.w)
            trooper.center_y = random.randrange(trooper.h, SH - trooper.h)
            self.trooper_list.append(trooper)

    def on_draw(self):
        arcade.start_render()
        if self.current_state == 0:
            arcade.draw_rectangle_filled(SW // 2, SH // 2, SW, SH, arcade.color.BLACK)
            arcade.draw_text("Use arrow keys to move BB8 and use SPACE to shoot.  Choose level 1, 2, or 3.",
                             SW / 2 - 290, SH / 2, (0, 255, 0), 14)

        elif self.game_running is True:
            arcade.draw_texture_rectangle(SW // 2, SH // 2, SW, SH, self.background)
            self.trooper_list.draw()
            self.player_list.draw()
            self.bullet_list.draw()
            self.explosions.draw()
            self.ebullets.draw()

            arcade.draw_lrtb_rectangle_filled(SW - 95, SW, SH, SH - 35, arcade.color.WHITE)
            output = f"Level: {self.current_state}"
            arcade.draw_text(output, SW - 90, SH - 15, arcade.color.BLACK, 14)
            output = f"Score: {self.score}"
            arcade.draw_text(output, SW - 90, SH - 30, arcade.color.BLACK, 14)

        else:       # draw game over screen
            output = f"Score: {self.score}"
            arcade.draw_rectangle_filled(SW // 2, SH // 2, SW, SH, arcade.color.BLACK)
            arcade.draw_text("Game over! Choose level 1, 2, or 3 to play again!", SW / 2 - 150, SH / 2, (0, 255, 0), 14)
            arcade.draw_text("Press I for instructions.", SW / 2 - 90, SH / 2 - 20, (0, 255, 0), 14)
            arcade.draw_text(output, SW / 2 - 35, SH / 2 - 40, arcade.color.WHITE, 14)

    def on_key_press(self, key, modifiers: int):
        if key == arcade.key.LEFT and self.game_running:
            self.BB8.change_angle = Angle_Speed
        elif key == arcade.key.RIGHT and self.game_running:
            self.BB8.change_angle = -Angle_Speed
        elif key == arcade.key.UP and self.game_running:
            self.BB8.speed = Movement_Speed
        elif key == arcade.key.DOWN and self.game_running:
            self.BB8.speed = -Movement_Speed
        elif key == arcade.key.SPACE and self.game_running:
            self.bullet = Bullet()
            self.bullet.center_x = self.BB8.center_x
            self.bullet.center_y = self.BB8.center_y
            self.bullet.angle = self.BB8.angle + 90
            self.bullet.speed = Bullet_Speed
            self.bullet_list.append(self.bullet)
            arcade.play_sound(self.BB8.laser_sound)
            self.score += Bullet_Points

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
        if (key == arcade.key.LEFT or key == arcade.key.RIGHT) and self.game_running:
            self.BB8.change_angle = 0
        if (key == arcade.key.UP or key == arcade.key.DOWN) and self.game_running:
            self.BB8.speed = 0

    def on_update(self, dt):
        if self.current_state > 0 and self.current_state < 4:
            self.game_running = True

        else:
            self.game_running = False

        if self.game_running is True:

            self.player_list.update()
            self.trooper_list.update()
            self.bullet_list.update()
            self.explosions.update()
            self.ebullets.update()

            if len(self.trooper_list) == 0:
                self.current_state += 1
                self.setup()

            self.bb8_hit = arcade.check_for_collision_with_list(self.BB8, self.trooper_list)
            # check if bb8 is colliding with a trooper
            if len(self.bb8_hit) > 0:
                self.BB8.kill()
                self.current_state = 4

            for trooper in self.trooper_list:
                if random.randrange(800) == 0:
                    ebullet = EnemyBullet()
                    ebullet.center_x = trooper.center_x
                    ebullet.center_y = trooper.center_y
                    self.ebullets.append(ebullet)

            for bullet in self.bullet_list:
                # check if a bullet and trooper are colliding
                hit_list = arcade.check_for_collision_with_list(bullet, self.trooper_list)

                if len(hit_list) > 0:
                    explosion = Explosion(self.explosion_texture_list)
                    explosion.center_x = hit_list[0].center_x
                    explosion.center_y = hit_list[0].center_y
                    self.explosions.append(explosion)
                    arcade.play_sound(explosion.explosion_sound)
                    bullet.kill()

                for trooper in hit_list:
                    trooper.kill()
                    self.score += Trooper_Points

            bb8_hit = arcade.check_for_collision_with_list(self.BB8, self.ebullets)
            if len(bb8_hit) > 0:
                arcade.play_sound(self.BB8.explosion_sound)
                self.BB8.kill()
                bb8_hit[0].kill()
                self.current_state = 4


# -----Main Function--------
def main():
    window = MyGame(SW, SH, "BB8 Attack")
    arcade.run()


# ------Run Main Function-----
if __name__ == "__main__":
    main()
