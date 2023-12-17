import pygame as pg
import numpy as np
from math import pi, sin, cos
from rotating_ascii_earth_for_image import Projection
from rotating_ascii_earth_for_image import Object

clock = pg.time.Clock()
FPS = 30

WIDTH = 800
HEIGHT = 800

R = 250
MAP_WIDTH = 139
MAP_HEIGHT = 34

pg.init()

my_font = pg.font.SysFont('arial', 20)

with open('image2.txt', 'r') as file:
    data = [file.read().replace('\n', '')]

ascii_chars = []
for line in data:
    for char in line:
        ascii_chars.append(char)

inverted_ascii_chars = ascii_chars[::-1]

xyz = []

for i in range(MAP_HEIGHT + 1):
    lat = (pi / MAP_HEIGHT) * i  #finally found reason image was wrogly displayed i have put "+" instead of "*"
    for j in range(MAP_WIDTH + 1):
        lon = (2 * pi / MAP_WIDTH) * j
        x = round(R * sin(lat) * cos(lon), 2)
        y = round(R * sin(lat) * sin(lon), 2)
        z = round(R * cos(lat), 2)
        xyz.append((x, y, z))

spin = 0.01
running = True

pv = Projection(WIDTH, HEIGHT)
globe = Object()
globe_nodes = [i for i in xyz]
globe.addNodes(np.array(globe_nodes))
pv.addSurface('globe', globe)

while running:
    dt = clock.tick(FPS)/10000.0

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    pv.screen.fill(pv.background)
    globe.rotate(globe.findCenter(), np.array([[cos(spin), -sin(spin), 0, 0],
                                               [sin(spin), cos(spin), 0, 0],
                                               [0, 0, 1, 0],
                                               [0, 0, 0, 1]]))
    pv.display()

    pg.display.update()
    spin += 0.01 * dt