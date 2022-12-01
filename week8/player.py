from math import sin
from enemy import *
from settings import *
from support import import_folder

pygame.init()

bullet_img = pygame.image.load('../graphics/gun/yeet.png')
bullet_img_red = pygame.image.load('../graphics/gun/yeet_red.png')
bullet_img_flip_red = pygame.transform.flip(bullet_img_red, True, False)
bullet_img_blue = pygame.image.load('../graphics/gun/yeet_blue.png')
bullet_img_flip_blue = pygame.transform.flip(bullet_img_blue, True, False)
bullet_img_green = pygame.image.load('../graphics/gun/yeet_green.png')
bullet_img_flip_green = pygame.transform.flip(bullet_img_green, True, False)
bullet_img_flip = pygame.transform.flip(bullet_img, True, False)
bullet_group = pygame.sprite.Group()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, image, colour):
        self.colour = colour
        pygame.sprite.Sprite.__init__(self)
        self.speed = 6
        if (colour==1):
            self.image = image
        if (colour==0):
            self.image = image
        elif (colour==2):
            self.image = image
        else:
            self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.pos = (self.rect.x, self.rect.y)
        self.bcolour = None

        #print(self.colour)

    def bullet_Colour(self):
        if self.colour == 1:
            self.bcolour = "red"
        if self.colour == 2:
            self.bcolour = "blue"
        if self.colour == 3:
            self.bcolour = "green"
        return (self.bcolour)

    def update(self):
        self.rect.x += self.direction * self.speed
        # bullet screen check
        if self.rect.right < 0 or self.rect.left > screen_width:
            self.kill()
        self.bullet_Colour()

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, create_jump_particles, change_health):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # dust particles
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles

        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16
        self.collision_rect = pygame.Rect(self.rect.topleft, (50, self.rect.height))

        # player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        # health management
        self.change_health = change_health
        self.invincible = False
        self.invincibility_duration = 500
        self.hurt_time = 0

        # audio
        self.jump_sound = pygame.mixer.Sound('../audio/effects/jump.wav')
        self.jump_sound.set_volume(0.5)
        self.hit_sound = pygame.mixer.Sound('../audio/effects/hit.wav')

        # shoot
        self.shoot_cooldown = 0

    def get_direction(self):
        return self.direction

    def import_character_assets(self):
        character_path = '../graphics/character/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder('../graphics/character/dust_particles/run')

    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
            self.rect.bottomleft = self.collision_rect.bottomleft
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
            self.rect.bottomright = self.collision_rect.bottomright

        if self.invincible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(6, 10)
                self.display_surface.blit(dust_particle, pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6, 10)
                flipped_dust_particle = pygame.transform.flip(dust_particle, True, False)
                self.display_surface.blit(flipped_dust_particle, pos)

    def bullet_create_red(self, colour):
        if self.facing_right:
            if self.shoot_cooldown == 0:
                self.shoot_cooldown = 20
                bullet = Bullet(self.rect.centerx + 40, self.rect.centery + 13, 1, bullet_img_red, colour)
                bullet_group.add(bullet)
        if not self.facing_right:
            if self.shoot_cooldown == 0:
                self.shoot_cooldown = 20
                bullet = Bullet(self.rect.centerx - 40, self.rect.centery + 13, -1, bullet_img_flip_red, colour)
                bullet_group.add(bullet)

    def bullet_create_blue(self, colour):
        if self.facing_right:
            if self.shoot_cooldown == 0:
                self.shoot_cooldown = 20
                bullet = Bullet(self.rect.centerx + 40, self.rect.centery + 13, 1, bullet_img_blue, colour)
                bullet_group.add(bullet)
        if not self.facing_right:
            if self.shoot_cooldown == 0:
                self.shoot_cooldown = 20
                bullet = Bullet(self.rect.centerx - 40, self.rect.centery + 13, -1, bullet_img_flip_blue, colour)
                bullet_group.add(bullet)

    def bullet_create_green(self, colour):
        if self.facing_right:
            if self.shoot_cooldown == 0:
                self.shoot_cooldown = 20
                bullet = Bullet(self.rect.centerx + 40, self.rect.centery + 13, 1, bullet_img_green, colour)
                bullet_group.add(bullet)
        if not self.facing_right:
            if self.shoot_cooldown == 0:
                self.shoot_cooldown = 20
                bullet = Bullet(self.rect.centerx - 40, self.rect.centery + 13, -1, bullet_img_flip_green, colour)
                bullet_group.add(bullet)

    def bullet_create(self, colour):
        if self.facing_right:
            if self.shoot_cooldown == 0:
                self.shoot_cooldown = 20
                bullet = Bullet(self.rect.centerx + 40, self.rect.centery + 13, 1, bullet_img, colour)
                bullet_group.add(bullet)
        if not self.facing_right:
            if self.shoot_cooldown == 0:
                self.shoot_cooldown = 20
                bullet = Bullet(self.rect.centerx - 40, self.rect.centery + 13, -1, bullet_img_flip, colour)
                bullet_group.add(bullet)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_e]:
            self.bullet_create(0)
        if keys[pygame.K_r]:
            self.bullet_create_red(1)
        if keys[pygame.K_b]:
            self.bullet_create_blue(2)
        if keys[pygame.K_g]:
            self.bullet_create_green(3)
        if keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
            self.create_jump_particles(self.rect.midbottom)

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.collision_rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed
        self.jump_sound.play()

    def get_damage(self):
        if not self.invincible:
            self.hit_sound.play()
            self.change_health(-10)
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()

    def invincibility_timer(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        self.invincibility_timer()
        self.wave_value()
        # update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

#create new instance
