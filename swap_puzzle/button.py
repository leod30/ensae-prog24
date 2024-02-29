"""
A button class that generates buttons based on an image
"""

import pygame

#button class
class Button():
  def __init__(self, x, y, image, scale, hover = None):
    width = image.get_width()
    height = image.get_height()
    self.zoom = 1.05
    self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
    if hover is not None:
      self.hover = pygame.transform.scale(hover, (int(width * scale*self.zoom), int(height * scale*self.zoom)))
    else:
      self.hover = None

    self.rect = self.image.get_rect()

    xx = self.rect.width
    yy = self.rect.height
    self.rect.topleft = (x - xx/2, y - yy/2)
    self.clicked = False

  def draw(self, surface):
    action = False
    #get mouse position
    pos = pygame.mouse.get_pos()

    #check mouseover and clicked conditions
    if self.rect.collidepoint(pos):
      if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
        self.clicked = True
        action = True

    if pygame.mouse.get_pressed()[0] == 0:
      self.clicked = False

    #draw button on screen
    if self.hover is not None and self.rect.collidepoint(pos):
      deltax, deltay = (self.zoom-1)/2*self.rect.width, (self.zoom-1)/2*self.rect.height
      surface.blit(self.hover, (self.rect.x - deltax, self.rect.y - deltay))
    else:
      surface.blit(self.image, (self.rect.x, self.rect.y))
    
    return action