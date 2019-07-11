import pygame
import random
import time

class Pipe:
   def __init__(self, window_height, window_width):
      self.x = window_width  # Current Position

      self.windowHeight = window_height
      self.windowWidth = window_width

      self.width = 70  # Pipe Width
      self.speed = 3.5  # Speed at which pipe moves

      self.color = (48, 142, 1)

      self.passed = False  # Flag to check wheter we've passed the bird or not

      self.gap = 50  # Gap between top and bottom part of pipe

      self.start = random.randint(0, window_height)  # Get a center value for the center of the gap between the pipes
      while self.start < 60 or self.start > self.windowHeight - 60:  # Change these values to alter the min/max height of the pipes
         self.start = random.randint(0, window_height)

      self.top = self.start - self.gap
      self.bottom = (self.start + self.gap) - window_height

   # Check collision with the player
   def checkCollision(self, bird):
      if bird.position[1] - 15 <= self.top or bird.position[
         1] + 15 >= self.bottom + self.windowHeight:  # Check if bird is in the same height as either the top or bottom of the pipe
         if bird.position[0] + 15 > self.x and bird.position[
            0] - 15 < self.x + self.width:  # Check if the bird is touching either the leftmost part or interior of the pipe
            return True

   # Update the pipe position
   def update(self, bird):
      self.x = self.x - int(self.speed)

      if self.passed is False and self.checkCollision(bird):
         return True

      return False

   # Draw both bottom and top parts of the pipe
   def draw(self, surface):
      # Bottom
      pygame.draw.rect(surface, self.color, (self.x, self.windowHeight, self.width, self.bottom))
      # Top
      pygame.draw.rect(surface, self.color, (self.x, 0, self.width, self.top))


class Bird():
   def __init__(self, size, window_height, window_width):
      self.size = size  # Bird size

      self.color = (239, 177, 49)

      self.position = [window_width / 6, window_height / 2]  # Position of the center of the bird

      self.maxHeight = window_height  # Window Height

      self.gravity = 0.5  # Velocity increases overtime
      self.lift = -10  # How high we jump
      self.velocity = 0  # Used to change the position

   def handleKeys(self):
      self.velocity = self.velocity + self.lift

   def update(self):
      self.velocity = self.velocity + self.gravity
      self.velocity = self.velocity * 0.91  # Makes it so velocity increases incrementally
      self.position[1] = self.position[1] + self.velocity

      if self.position[1] + 5 >= self.maxHeight or self.position[1] - 5 <= 0:  # Check ground/ceilling collision
         return True

      return False

   def draw(self, surface):
      pygame.draw.circle(surface, self.color, (int(self.position[0]), int(self.position[1])), self.size)


def __init__():
   clock = pygame.time.Clock()

   pygame.init()
   screen = pygame.display.set_mode((500, 500))
   done = False

   # Create player
   player = Bird(15, screen.get_width(), screen.get_height())

   # Create pipes array and add first pipe
   pipes = []
   pipes.append(Pipe(screen.get_width(), screen.get_height()))


   score = 0
   delta_time = time.time()
   time_bt_pipes = 2  # 1 second

   while not done:
      screen.fill((76, 188, 252))

      # Player
      player.draw(screen)

      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            done = True
         if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
               player.handleKeys()
               # print("Jump")

      done = player.update()
      if done:
         break

      # Pipes
      if time.time() - delta_time >= time_bt_pipes:
         delta_time = time.time()
         pipes.append(Pipe(screen.get_width(), screen.get_height()))

      for pipe in pipes:
         pipe.draw(screen)
         done = pipe.update(player)

         if done:
            break

         # Check if pipe is off the screen or if it has passed the bird
         if pipe.x + pipe.width < 0:
            pipes.remove(pipe)
         elif pipe.passed is False and pipe.x + pipe.width < screen.get_width() / 6 - 15:
            score = score + 1
            pipe.passed = True

      font = pygame.font.Font(None, 36)
      text = font.render(str(score), 1, (255, 255, 255))
      textpos = text.get_rect(centerx=screen.get_width() / 2)
      screen.blit(text, textpos)

      pygame.display.update()
      clock.tick(60)


__init__()
