import random
from settings import *
import pygame
from tiles import AnimatedTile
from random import *

class Enemy(AnimatedTile):
	def __init__(self,size,x,y):
		self.colour = randint(1, 3)
		if(self.colour == 1):
			super().__init__(size,x,y,'../graphics/enemy/run_red')
		elif(self.colour == 2):
			super().__init__(size,x,y,'../graphics/enemy/run_blue')
		else:
			super().__init__(size,x,y,'../graphics/enemy/run_green')
		self.rect.y += size - self.image.get_size()[1]
		self.speed = randint(3,5)

	def Colour(self):
		if self.colour == 1:
			kolour = "red"
		if self.colour == 2:
			kolour = "blue"
		if self.colour == 3:
			kolour = "green"
		

	def move(self):
		self.rect.x += self.speed

	def reverse_image(self):
		if self.speed > 0:
			self.image = pygame.transform.flip(self.image,True,False)

	def reverse(self):
		self.speed *= -1

	def update(self,shift):
		self.rect.x += shift[0]
		self.rect.y += shift[1]
		self.animate()
		self.move()
		self.reverse_image()
		self.Colour()


#new instance

