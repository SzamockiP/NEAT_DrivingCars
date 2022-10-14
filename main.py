import os
import neat
import math
import pygame  
import random
# stale zmienne gry itp
WIN_WIDTH = 512  # rozmiar okna
WIN_HEIGHT = 512

CAR_SIZE = 50  # rozmiar auta(wysokosc, car_size/2 = szerokosc)
CAR_IMAGES = [pygame.transform.smoothscale(pygame.image.load(os.path.join('images', 'car_accelerating.jpg')), (round(CAR_SIZE/2), CAR_SIZE)), 
			pygame.transform.smoothscale(pygame.image.load(os.path.join('images', 'car_driving.jpg')), (round(CAR_SIZE/2), CAR_SIZE)),
			pygame.transform.smoothscale(pygame.image.load(os.path.join('images', 'car_breaking.jpg')), (round(CAR_SIZE/2), CAR_SIZE))]  # obrazki aut

ROAD_CONE_IMAGE = pygame.transform.smoothscale(pygame.image.load(os.path.join('images', 'road_cone.png')), (48,48))
ASPHALT_IMAGE = pygame.transform.smoothscale(pygame.image.load(os.path.join('images', 'asphalt_texture.jpg')), (WIN_WIDTH,WIN_WIDTH))
MAP_MOVE_VEL = 1  # szybkosc ruszania sie mapy w dol

class Car:
	IMGS = CAR_IMAGES  # stale zmienne w samochodach
	MAX_SPEED = 2
	STEERING_SPEED = 1
	CAN_BREAK = True
	SIZE = CAR_SIZE

	def __init__(self, position):  # inicjalizacja zmiennych
		self.x = position[0]
		self.y = position[1]

		self.vel = 0.0
		self.rotation = random.choice(range(-90,90,1))

		self.steering = 0  #  -1 left, 0 none, 1 right
		self.accelerating = False
		self.breaking = False

		self.image = self.IMGS[1]
		print('Made a car')


	def move(self, is_accelerating = False, is_breaking = False, steering = 0):  # hamowanie wazniejsze od przyspieszania jest, a przyspieszanie od spoczynku
		if is_breaking and self.vel >= 0:
			self.vel -= 0.01
			if self.vel < 0:
				self.vel = 0
			self.image = self.IMGS[2]  # zmien wyglad na hamowanie

		elif is_accelerating:
			if self.vel < self.MAX_SPEED:
				self.vel += 0.01
				self.image = self.IMGS[0]  # zmien wyglad na przyspieszanie

		else:
			self.image = self.IMGS[1]  # zmien wyglad na normalny

		self.rotation += steering * self.STEERING_SPEED

		# to po prostu funkcja ktora przeksztalca stopnie na wartosci od 1 do -1
		def deg_to_direction(x):
			if(x%360<180): 
				return 1-((x % 180)/180)*2
			else:
				return ((x % 180)/180)*2-1

		self.x -= self.vel * round(deg_to_direction(self.rotation-90),2)  # zmiana pozycji aut na x i y
		self.y -= self.vel * round(deg_to_direction(self.rotation),2) - MAP_MOVE_VEL


	def draw(self, window):
		rotated_image = pygame.transform.rotate(self.image, self.rotation)  # obrot obrazka
		new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=(self.x, self.y)).center)  # troche chuj wie czego

		window.blit(rotated_image, (new_rect[0]-self.SIZE/4, new_rect[1]-self.SIZE/2))  # narysuj na pozycji od srodka samochodu  


	def get_mask(self):
		pass


class Road():
	VEL = MAP_MOVE_VEL
	IMG = ASPHALT_IMAGE
	HEIGHT = IMG.get_height()

	def __init__(self):
		self.y1 = 0
		self.y2 = -self.HEIGHT

	def move(self):
		self.y1 += self.VEL
		self.y2 += self.VEL

		if self.y1 > self.HEIGHT:
			self.y1 = -self.HEIGHT
		
		if self.y2 > self.HEIGHT:
			self.y2 = -self.HEIGHT

	def draw(self, window):
		window.blit(self.IMG, (0, self.y1))
		window.blit(self.IMG, (0, self.y2))


def draw_window(window, cars_list, road):
	# window.fill((255, 255, 255)) # biale tlo
	road.draw(window)  
	for car in cars_list:  # narysuj auta
		car.draw(window)

	pygame.display.update()  # update ekranu


def main():
	cars = [Car((256,412)) for x in range(50)]  # utworz liste aut
	win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))  # init ekrany
	asphalt_road = Road()

	clock = pygame.time.Clock()

	running = True

	while running:
		# clock.tick(30)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False  # petla od wyjscia
		for car in cars:
			car.move(True,False,0)
		asphalt_road.move()
		draw_window(win, cars, asphalt_road)  # narysuj wszystko na ekranie

if __name__ == '__main__':
	main()