#!user/bin/env pyton
# -*- coding: utf-8 -*-

import clases, pygame, random
from clases import ancho, alto, paleta, fondo, caveza, comida, txt, tam, escala

pygame.init()
exit = False

def main():
	ventana = pygame.display.set_mode((ancho, alto))
	pygame.display.set_caption("Snake")
	clock = pygame.time.Clock()
	myFont = pygame.font.SysFont("Elephant", 20)
	gameOver = pygame.font.SysFont("Fixedsys", 90)
	quit = False

	ml = 0
	seg = 0
	m = 0
	h = 0
	pts = 0

	s = clases.serpiente((tam/2)*escala, (tam/2)*escala)
	c = clases.manzana(random.randint(0, tam)*escala, random.randint(0, tam)*escala)

	fin = gameOver.render("Game Over", 1, paleta[txt])

	while not quit:
		if seg >=60:
			seg = 0
			m += 1
			if m >= 60:
				m = 0
				h += 1
		time = myFont.render("{0:0>2}:{1:0>2}:{2:0>2}".format(h, m, seg), 1, paleta[txt])
		puntos = myFont.render("Puntos: {0}".format(pts), 1, paleta[txt])

		for event in pygame.event.get():
			if event.type == pygame.QUIT: quit = True
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: quit = True
			s.handle(event)

		if c.crea(s.comer(c)):
			pts += 3
		s.mueve()
		if s.fuera(): quit = True

		ventana.fill(paleta[fondo])
		ventana.blit(time, (490, 10))
		ventana.blit(puntos, (10, 10))
		c.pinta(ventana)
		s.pinta(ventana)
		if s.me_comi(): quit = True
		pygame.display.update()
		clock.tick(10)

		if ml >= 10:
			seg += 1
			ml = 0
		ml += 1

	pos = fin.get_size()
	x = (ancho/2)-(pos[0]/2)
	y = (alto/2)-(pos[1]/2)
	ventana.blit(fin, (x, y))
	pygame.display.update()
	pygame.time.delay(600)
	pygame.quit()

main()
