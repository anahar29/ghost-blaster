# Bring over all your Checkpoint 1 work here and then continue
# working from this Repl.it
##
# Pygame base template for opening a window - MVC version
# Simpson College Computer Science
# http://programarcadegames.com/
#


# Does 15 ghosts but one at a time
# collision is off


## Pygame setup
import pygame
import math
import random

# subprograms

# Equation from Mr. Reid
def checkCollision(ghostX, ghostY, bulletX, bulletY):

    result = False
    tolerance = 50
    if (abs(ghostX - bulletX) < tolerance
        and abs(ghostY - bulletY) < tolerance):
        # What do you want to happen?
        result = True
    return result


pygame.init()
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Ghost Blaster")

## MODEL - Data use in system
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
score = 0
bgpos = [0, 0]
# Defining variables
pos = [380, 490]

ghostList = []

# Shooter variables
shooterX = 380
shooterY = 490
shooterMove = 0

font = pygame.font.Font('freesansbold.ttf', 16)

class Rectangle():
    x = 0
    y = 0
    width = 10
    height = 10
    change_x = 2
    change_y = 2
    color = [0, 0, 0]

    def __init__(self):
        self.x = random.randrange(0, 700)
        self.y = random.randrange(0, 500)
        self.change_x = random.randrange(-3., 3)
        self.change_y = random.randrange(-3., 3)
        self.width = 10
        self.height = 10
        self.color = [0, 0, 0]
        self.color = [random.randrange(0, 256) for _ in range(3)]


    def draw(self, screen):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height], 0)

    def move(self):
        if self.x < 0:
            self.change_x *= -1
        if self.x > 700-self.width:
            self.change_x *= -1
        if self.y < 0:
            self.change_y *= -1
        if self.y > 500-self.height:
            self.change_y *= -1
        self.x += self.change_x
        self.y += self.change_y

# child class (ellipse shape)
class Ellipse(Rectangle):
    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, [self.x, self.y, self.width, self.height], 0)



# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Load images
classList = []

# rectangle loop
for i in range(50):
    classList.append(Rectangle())

# ellipse loop
for i in range(50):
    classList.append(Ellipse())

# Set player shooter
shooter = pygame.image.load("shooter.webp").convert()
shooter.set_colorkey(BLACK)
shooter = pygame.transform.scale(shooter, (160, 160))

# Enemy ghosts
ghosty = pygame.image.load("pacy.png").convert()
ghosty.set_colorkey(BLACK)
ghosty= pygame.transform.scale(ghosty, (70, 70))
# Ghost's random movements
ghostMoveX = 0 #4
ghostMoveY = 0 #50

for i in range (15):
    ghostX = random.randrange(0, 650)
    ghostY = random.randrange(50, 390)
    ghostList.append([ghostX, ghostY])

# Bullets - "False" means bullet is not in motion
bulletPic = pygame.image.load("bullet (1).png")
bulletX = 0
bulletY = 490
#bulletXChange =
bulletYChange = 20
bulletMode = False

# Bullet's movement
def shootBullet(x, y):
    global bulletMode # find alternative
    bulletMode = True
    screen.blit(bulletPic, [x+60, y+20])

def image(image, x, y):
    screen.blit(image,[x, y])

def gameOver():
    text = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(text, (200, 250))
    done = False


## Main Program Loop
while not done:
    ## CONTROL
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                  shooterMove = -7
            if event.key == pygame.K_RIGHT:
                  shooterMove = 7
            if event.key == pygame.K_SPACE:
              if bulletMode == False:
                  bulletX = shooterX
                  shootBullet(bulletX, bulletY)
        elif (event.type == pygame.KEYUP):
            shooterMove = 0


    shooterX += shooterMove
    if shooterX <= 0:
        shooterX = 0
    elif shooterX >= 650:
        shooterX = 650

    # Movement
    for ghost in ghostList:
        ghost[0] += 3

        if ghost[0] <= 0:
           # ghostMoveX = 3
            ghost[0] = 0
            ghost[0] += 0.3
        elif ghost[0] >= 650:
           # ghostMoveX = -3
            ghost[0] = -7
            ghost[1] += 25
        elif ghost[1] >= 490:
            ghost[1] = 490
            text = font.render("GAME OVER", True, (255, 255, 255))
            screen.blit(text, (200, 250))
            done = True



            # Collisions !
    if bulletMode == True:
        for ghost in ghostList:
            collisions = checkCollision(ghost[0], ghost[1], bulletX, bulletY)
            if collisions:
                #ghostList.remove(ghost)
                bulletY = 480
                bulletMode = False
                score+= 2
                ghost[0] = random.randrange(0, 736)
                ghost[1] = random.randrange(0, 450)

    ## VIEW
    # Clear screen
    screen.fill(BLACK)
    background = pygame.image.load("space.webp").convert()
    background.set_colorkey(BLACK)
    background = pygame.transform.scale(background, (800, 600))
    screen.blit(background, bgpos )

    for shape in classList:
        shape.draw(screen)
        shape.move()

    # Draw
  # Bullet movement
    if bulletY <= 10:
      bulletY = 480
      bulletMode = False

    if bulletMode == True:
       shootBullet(bulletX, bulletY)
       bulletY -= bulletYChange



    image(shooter, shooterX, shooterY)

    for ghost in ghostList:
        image(ghosty, ghost[0], ghost[1])


    # Update Screen
    pygame.display.flip()
    clock.tick(60)

# Close the window and quit
pygame.quit()
