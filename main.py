#coding=utf-8  
import random  
from random import randrange, choice
from collections import defaultdict
import sys  
import pygame  
from pygame.locals import * 

PIXEL = 150
SCORE_PIXEL = 100

actions = ['Up', 'Left', 'Down', 'Right']
def transpose(field):
	return [list(row) for row in zip(*field)]

def invert(field):
	return [row[::-1] for row in field]

class GameField(object):
	def __init__ (self, height = 4, width = 4, judgement = 2048):
		self.height = height
		self.width = width
		self.judgement = judgement
		self.curScore = 0
		self.higestScore = 0
		self.reset()

	def generator(self):
		if(randrange(100) > 77):
			new = 4
		else:
			new = 2
		(i, j) = choice([(i, j) for i in range(self.width) for j in range(self.height) if self.value[i][j] == 0])
		
                                   
		self.value[i][j] = new

	def reset(self):
		if(self.curScore > self.higestScore):
			self.higestScore = self.curScore
		self.curScore = 0
		self.value = [[0 for i in range(self.width)] for j in range(self.height)]
		self.generator()
		self.generator()

	

	def move(self, direction):
		def adjust_to_left(row):
			def push_to_left(row):
				new_row = [i for i in row if(i != 0)]
				new_row += [0 for i in range(len(row) - len(new_row))]
				return new_row

			def merge(row):
				pair = False
				new_row = []
				for i in range(len(row)):
					if(pair):
						new_row.append(2 * row[i])
						self.curScore += 2 * row[i]
						pair = False
					else:
						if(i < len(row) - 1 and row[i] == row[i + 1]):
							pair = True
							new_row.append(0)
						else:
							new_row.append(row[i])
				return new_row

			return push_to_left(merge(push_to_left(row)))

		moves = {}
		moves['Left'] = lambda value: [adjust_to_left(row) for row in value]
		moves['Right'] = lambda value: invert(moves['Left'](invert(value)))
		moves['Up'] = lambda value: transpose(moves['Left'](transpose(value)))
		moves['Down'] = lambda value: transpose(moves['Right'](transpose(value)))

		if(direction in moves):
			if(self.checkMove(direction)):
				self.value = moves[direction](self.value)
				self.generator()
				return True
			else:
				return False

	def checkMove(self, direction):
		def checkMove_left(row):
			def judge(i):
				if(row[i] == 0 and row[i + 1] != 0):
					return True
				if(row[i] != 0 and row[i] == row[i + 1]):
					return True
				return False
			return any(judge(i) for i in range(len(row) - 1))

		check = {}
		check['Left'] = lambda value: any(checkMove_left(row) for row in value)
		check['Right'] = lambda value: check['Left'](invert(value))
		check['Up'] = lambda value: check['Left'](transpose(value))
		check['Down'] = lambda value: check['Right'](transpose(value))

		if(direction in check):
			return check[direction](self.value)
		else:
			return False


	def isWin(self):
		return self.curScore >= self.judgement

	def isGameover(self):
		actions = ['Up', 'Left', 'Down', 'Right']
		return not any(self.checkMove(direction) for direction in actions)


def display(map, screen, block, map_font, score_block, score_font):
	for i in range(map.height):
		for j in range(map.width):
			screen.blit(map.value[i][j] == 0 and block[(i + j) % 2] or block[2 + (i + j) % 2], (PIXEL * j, PIXEL * i)) 
			#show points
			if(map.value[i][j] != 0):
				map_text = map_font.render(str(map.value[i][j]), True, (106, 90, 205))  
				text_rect = map_text.get_rect()  
				text_rect.center = (PIXEL * j + PIXEL / 2, PIXEL * i + PIXEL / 2)  
				screen.blit(map_text, text_rect)

	screen.blit(score_block, (0, PIXEL * map.height))  
	score_text = score_font.render((map.isGameover() and "Game over with score " or "Score: ") + str(map.curScore), True, (106, 90, 205))  
	score_rect = score_text.get_rect()  
	score_rect.center = (PIXEL * map.height / 2, PIXEL * map.height + SCORE_PIXEL / 2)  
	screen.blit(score_text, score_rect)  
	pygame.display.update()  


def main():
	map = GameField()
	pygame.init()
	screen = pygame.display.set_mode((PIXEL * map.height, PIXEL * map.height + SCORE_PIXEL))
	pygame.display.set_caption("2048")

	#colour set
	block = [pygame.Surface((PIXEL, PIXEL)) for i in range(4)]
	block[0].fill((152, 251, 152))
	block[1].fill((240, 255, 255))
	block[2].fill((0, 255, 127))
	block[3].fill((255, 255, 255))
	score_block = pygame.Surface((PIXEL * map.height, SCORE_PIXEL))
	score_block.fill((245, 245, 245))
	#colour set

	#font set
	map_font = pygame.font.Font(None, int(PIXEL * 2 / 3))
	score_font = pygame.font.Font(None, int(SCORE_PIXEL * 2 / 3))
	clock = pygame.time.Clock()
	display(map, screen, block, map_font, score_block, score_font)

	#font set

	while(not map.isGameover()):
		clock.tick(12)
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit();

		key = pygame.key.get_pressed()
		if(key[K_UP]):
			map.move('Up')
		elif(key[K_DOWN]):
			map.move('Down')
		elif(key[K_LEFT]):
			map.move('Left')
		elif(key[K_RIGHT]):
			map.move('Right')

		display(map, screen, block, map_font, score_block, score_font)
	pygame.time.delay(3000)


if __name__=="__main__":
	main()
