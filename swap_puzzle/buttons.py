"""
A button class that generates buttons from scratch
"""

import pygame
import time

#button class
class Button():
  def __init__(self, x, y, txt, txt_col, hover_col, font_size, border, radius = 8, padding_x = 25, padding_y = 30):
    self.zoom = 1.05
    self.padding_x = padding_x
    self.padding_y = padding_y

    self.font = pygame.font.SysFont("verdana bold", font_size)
    self.font_hover = pygame.font.SysFont("verdana bold", int(font_size*self.zoom))

    self.txt_col, self.hover_col, self.font_size, self.border, self.radius = txt_col, hover_col, font_size, border, radius

    self.txt = self.font.render(txt, True, txt_col)
    self.txt_hover = self.font_hover.render(txt, True, txt_col)

    self.x = x
    self.y = y
    self.xx = self.txt.get_rect().width
    self.yy = self.txt.get_rect().height

    self.xx_hover = self.txt_hover.get_rect().width
    self.yy_hover = self.txt_hover.get_rect().height

    self.clicked = False

  def draw(self, surface):
    self.clicked = False
    action = False
    
    #get mouse position
    pos = pygame.mouse.get_pos()

    #check mouseover and clicked conditions and draw button
    if pygame.Rect(self.x-(self.xx+self.padding_x)/2, self.y-(self.yy+self.padding_y)/2, self.xx+self.padding_x, self.yy+self.padding_y).collidepoint(pos):
      if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
        self.clicked = True
        action = True

      else:
        #deltax, deltay = (self.zoom-1)/2*self.txt_hover.get_rect().width, (self.zoom-1)/2*self.txt.get_rect().height
        pygame.draw.rect(surface, self.hover_col, (self.x-(self.xx_hover+self.padding_x)/2*self.zoom, self.y-(self.yy_hover+self.padding_y)/2*self.zoom, (self.xx_hover+self.padding_x)*self.zoom, (self.yy_hover+self.padding_y)*self.zoom), width = 0, border_radius = self.radius)
        pygame.draw.rect(surface, self.txt_col, (self.x-(self.xx_hover+self.padding_x)/2*self.zoom, self.y-(self.yy_hover+self.padding_y)/2*self.zoom, (self.xx_hover+self.padding_x)*self.zoom, (self.yy_hover+self.padding_y)*self.zoom), width = self.border, border_radius = self.radius)

      #display text
      surface.blit(self.txt_hover, (self.x-self.xx_hover/2, self.y-self.yy_hover/2))

    else:
      pygame.draw.rect(surface, self.txt_col, (self.x-(self.xx+self.padding_x)/2, self.y-(self.yy+self.padding_y)/2, (self.xx+self.padding_x), (self.yy+self.padding_y)), width = self.border, border_radius = self.radius)

      #display text
      surface.blit(self.txt, (self.x-self.xx/2, self.y-self.yy/2))

    return action