import pygame
import random

# Global constants

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Screen dimensions
WIDTH = 600
HEIGHT = 1000

class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
        controls. """

    # -- Methods
    def __init__(self):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        width = 40
        height = 60

        self.image = pygame.image.load("assets/pngwing.comMINION.png")
        self.image = pygame.transform.scale(self.image, [50,50])

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

        #jump bools
        self.canJump = True
        self.canDouble = True

        # List of sprites we can bump against
        self.level = None


    def update(self, platform_list):
        """ Move the player. """
        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything in the vertical axis
        block_hit_list = pygame.sprite.spritecollide(self, platform_list, False)

        if self.change_y < 0:
            self.image = pygame.image.load("assets/purble.png")
            self.image = pygame.transform.scale(self.image, [120, 70])
        else:
            self.image = pygame.image.load("assets/pngwing.comMINION.png")
            self.image = pygame.transform.scale(self.image, [50,50])

        for block in block_hit_list:
            #reset jump bools
            self.canJump = True
            self.canDouble = True

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top

            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .25

        # See if we are on the ground.
        if self.rect.y >= HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = HEIGHT - self.rect.height

    def jump(self, platform_list):
        """ Called when user hits 'jump' button. """

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if self.canJump:
            self.canJump = False
            self.change_y = -10
        elif self.canDouble:
            self.canDouble = False
            self.change_y = -7

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0

class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        W = 140
        H = 15
        self.image = pygame.image.load("./assets/pngwing.comROCK.png")
        self.image = pygame.transform.scale(self.image, [120,20])
        self.rect = self.image.get_rect()

        self.yvel = random.randrange(1,4)

    def update(self):
        self.rect.y += self.yvel

        if self.rect.y > (HEIGHT - 100):
            self.rect.y = random.randrange(-20,10)
            self.rect.x = random.randrange(0, (WIDTH - 70))

class Lava(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./assets/d9xal3j-444865d1-08cb-446e-be9c-647183b6efc4.png")
        self.image = pygame.transform.scale(self.image, [WIDTH, 100])

        self.rect = self.image.get_rect()

def main():
    pygame.init()

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Cave In")

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()
    score = 0
    default_font = pygame.font.SysFont("Menlo", 20)
    titleFont = pygame.font.SysFont('impact', 100)
    start = False
    jump_sound = pygame.mixer.Sound("./assets/jump.ogg")

    #determines platform number
    if score > 2000:
        platformNum = 6
    elif score > 4000:
        platformNum = 5
    else:
        platformNum = 7

    #groups
    lava_sprite = pygame.sprite.Group()
    platform_Sprites = pygame.sprite.Group()
    all_sprites_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    collided_enemy = pygame.sprite.Group()

    #create player
    player = Player()
    player.rect.x = 275
    player.rect.y = WIDTH/2
    player_group.add(player)

    #create new platforms
    for i in range(platformNum):
        pf = platform()
        x,y = (random.randrange(10, WIDTH-60),
               random.randrange((HEIGHT//platformNum * i+1),
                                (HEIGHT//platformNum * (i+1))))
        pf.rect.center = (x,y)
        platform_Sprites.add(pf)
        all_sprites_group.add(pf)

    #create lava
    lava = Lava()
    x,y = (0, HEIGHT - 100)
    lava.rect.center = ((WIDTH//2), HEIGHT-50)
    lava_sprite.add(lava)
    all_sprites_group.add(lava)


    while start is False:
        screen.fill(BLACK)
        bg = pygame.image.load("./assets/pngegg.png")
        bg = pygame.transform.scale(bg, [WIDTH, HEIGHT])
        startScreen = default_font.render("Click to start", True, WHITE)
        sSWIDTH = startScreen.get_width()
        startTitle = titleFont.render("CAVE IN", True, RED)
        sTWIDTH = startTitle.get_width()
        startINSTRUC1 = default_font.render("The cave youre mining in collapses!", True, WHITE)
        startINSTRUC2 = default_font.render("Jump your way home to Gru-oppar!", True, WHITE)
        sI1WIDTH = startINSTRUC1.get_width()
        sI2WIDTH = startINSTRUC2.get_width()
        screen.blit(bg, (0,0))
        screen.blit(startTitle, (300 - (sTWIDTH // 2), 300))
        screen.blit(startScreen, (300 - (sSWIDTH // 2), 800))
        screen.blit(startINSTRUC1, (300 - (sI1WIDTH // 2), 500))
        screen.blit(startINSTRUC2, (300 - (sI2WIDTH // 2), 550))


        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                start = True
        pygame.display.flip()

    # ----- MAIN LOOP
    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_SPACE:
                    player.jump(platform_Sprites)
                    pygame.mixer.Sound.play(jump_sound)

        # ----- LOGIC
        if len(collided_enemy) == 0:
            all_sprites_group.update()
            player.update(platform_Sprites)

            if player.rect.right > WIDTH:
                player.rect.right = WIDTH

            if player.rect.left < 0:
                player.rect.left = 0

            collided_enemy.add(pygame.sprite.spritecollide(lava,player_group,
                                                         dokill=True))
            if len(collided_enemy) == 0:
                score += 1
            else:
                done = True

        # ----- RENDER
        screen.fill(BLACK)
        bg = pygame.image.load("./assets/nether_resized.jpg")
        # bg = pygame.transform.scale(bg, [WIDTH, HEIGHT])
        screen.blit(bg, (0, 0))

        #draw the sprites
        all_sprites_group.draw(screen)
        player_group.draw(screen)
        # platform_Sprites.draw(screen)

        score_surf = default_font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surf, (10, 10))

        # ----- UPDATE DISPLAY
        pygame.display.flip()
        clock.tick(60)

    finalScore = default_font.render(f"Your final score is {score}", True, WHITE)
    scoreWIDTH = finalScore.get_width()
    done = False

    if score < 3000:
        die_sound = pygame.mixer.Sound("./assets/AUUGHHH Sound Effect.mp3")
        pygame.mixer.Sound.play(die_sound)
    else:
        good_job_sound = pygame.mixer.Sound("./assets/piglevelwin2mp3-14800.ogg")
        pygame.mixer.Sound.play(good_job_sound)

    while done is False:
        while score < 3000:
            screen.fill(RED)
            sadBg = pygame.image.load("./assets/sad-gru.png")
            sadBg = pygame.transform.scale(sadBg, [WIDTH, HEIGHT//4])
            loseMessage = default_font.render(f"You died! Gru is upset with your performance", True, WHITE)
            loseWIDTH = loseMessage.get_width()
            screen.blit(sadBg, (0, HEIGHT//3))
            screen.blit(loseMessage, (300 - loseWIDTH // 2, 300))
            screen.blit(finalScore, (300 - scoreWIDTH // 2, (HEIGHT // 4) + (sadBg.get_height() + 10)))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

            pygame.display.flip()

        while score > 2999:
            screen.fill(GREEN)
            happyBg = pygame.image.load("./assets/106429653-1583525430557minonscropped.jpg")
            happyBg = pygame.transform.scale(happyBg, [WIDTH, HEIGHT // 4])
            winMessage = default_font.render(f"You died! Gru was very entertained ", True, WHITE)
            winWIDTH = winMessage.get_width()
            screen.blit(happyBg, (0, HEIGHT // 3))
            screen.blit(winMessage, (300 - winWIDTH // 2, 300))
            screen.blit(finalScore, (300 - scoreWIDTH // 2, (HEIGHT // 4) + (happyBg.get_height() + 10)))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

            pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()