#!user/bin/env python
# -*- coding: utf-8 -*-

import pygame, random

tam = 60
escala = 10

ancho = tam*escala
alto = tam*escala

paleta = [(47, 79, 79),(255, 195, 0), (255, 87, 51), (199, 0, 57), (144, 12, 63)]
fondo = 0
caveza = 1
cuerpo = 2
comida = 3
txt = 4

class pixel(object):
	def __init__(self, x=0, y=0, w=escala, h=escala, c=(255, 255, 255)):
		self.r = pygame.Rect(x, y, w, h)
		self.color = c
		self.movx = 0
		self.movy = 0
		self.speed = 10

	def pinta(self, ventana):
		pygame.draw.rect(ventana, self.color, self.r)

	def mueve(self):
		self.r.move_ip(self.movx, self.movy)

	def dentro(self, rect):
		return self.r.colliderect(rect)

class serpiente(pixel):
	def __init__(self, x=0, y=0, w=10, h=10, c=(255, 255, 255)):
		pixel.__init__(self, x, y, w, h, c)
		self.color = paleta[caveza]
		self.cuerpo = []
		self.beep = pygame.mixer.Sound("sound/Beep.wav")

	def handle(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT and self.movx >= 0:
				self.movx = self.speed
				self.movy = 0
			if event.key == pygame.K_LEFT and self.movx <= 0:
				self.movx = -self.speed
				self.movy = 0
			if event.key == pygame.K_DOWN and self.movy >= 0:
				self.movy = self.speed
				self.movx = 0
			if event.key == pygame.K_UP and self.movy <= 0:
				self.movy = -self.speed
				self.movx = 0

	def pinta(self, ventana):
		pixel.pinta(self, ventana)
		for i in self.cuerpo:
			pygame.draw.rect(ventana, paleta[cuerpo], i)

	def mueve(self):
		l = len(self.cuerpo)
		for i in range(l-1, 0, -1):
			self.cuerpo[i].clamp_ip(self.cuerpo[i-1])
		if l > 0:
			self.cuerpo[0].clamp_ip(self.r)
		pixel.mueve(self)

	def me_comi(self):
		for i in self.cuerpo:
			if self.dentro(i): return True
		return False

	def comer(self, c):
		if self.dentro(c.r):
			self.cuerpo.append(pygame.Rect(self.r))
			self.beep.play()

			libre = False
			while not libre:
				r = pygame.Rect(random.randint(0, tam-1)*escala, random.randint(0, tam-1)*escala, 10, 10)
				if self.dentro(r): libre = True
				for i in self.cuerpo:
					if i.colliderect(r): libre = True
				if not libre: return [r.x, r.y]
		return None

	def fuera(self):
		r = pygame.Rect(0, 0, ancho, alto)
		if not self.dentro(r):
			return True
		return False

class manzana(pixel):
	def __init__(self, x=0, y=0, w=10, h=10, c=(255, 255, 255)):
		pixel.__init__(self, x, y, w, h, c)
		self.color = paleta[comida]

	def crea(self, pos):
		if pos != None:
			self.r.x = pos[0]
			self.r.y = pos[1]
			return True
		return False
