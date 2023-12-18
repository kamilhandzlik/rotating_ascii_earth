import pygame as pg
import numpy as np
from math import pi, sin, cos

clock = pg.time.Clock()
FPS = 30

WIDTH = 800
HEIGHT = 800

R = 220
R_of_moon = R/3.7
MAP_WIDTH = 139
MAP_HEIGHT = 40
MAP_MOON_WIDTH = 49
MAP_MOON_HEIGHT = 15


black = (0, 0, 0, )
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (100, 100, 100)
dark_grey = (50, 50, 50)

pg.init()

my_font = pg.font.SysFont('arial', 20)
my_font_moon = pg.font.SysFont('arial', 12)

with open('image.txt', 'r') as file:
    data = [file.read().replace('\n', '').replace(' ', '.')]

ascii_chars = []
for line in data:
    for char in line:
        ascii_chars.append(char)

inverted_ascii_chars = ascii_chars[::-1]

with open('moon.txt', 'r') as file:
    data = [file.read().replace('\n', '').replace(' ', '.')]

moon_ascii_chars = []
for line in data:
    for char in line:
        moon_ascii_chars.append(char)

inverted_moon_ascii_chars = ascii_chars[::-1]

class Projection:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pg.display.set_mode((width, height))
        self.background = black
        pg.display.set_caption('ASCII 3D EARTH')
        self.surfaces = {}

    def addSurface(self, name, surface):
        self.surfaces[name] = surface

    def display(self):
        self.screen.fill(self.background)

        for key, value in self.surfaces.items():
            if key == 'earth':
                i = 0
                for node in value.nodes:
                    self.text = inverted_ascii_chars[i]
                    self.text_surface = my_font.render(self.text, False, (blue if self.text == "." else green))
                    if node[1] >0:
                        self.screen.blit(self.text_surface, (WIDTH / 2 + int(node[0]), HEIGHT / 2 + int(node[2])))
                    i += 1
            elif key == 'moon':
                j = 0
                for node in value.nodes:
                    self.text = inverted_moon_ascii_chars[i]
                    self.text_surface = my_font.render(self.text, False, (blue if self.text == "." else green))
                    if j > MAP_MOON_WIDTH - 1 and i < (MAP_MOON_WIDTH * MAP_MOON_HEIGHT - MAP_MOON_WIDTH) and node[1] > 0:
                        self.screen.blit(self.text_surface, (WIDTH / 2 + int(node[0]), HEIGHT / 2 + int(node[2])))
                    j += 1

    def rotateAll(self, theta):
        for surface in self.surfaces.values():
            center = surface.findCenter()
            c = np.cos(theta)
            s = np.sin(theta)
            # Rotation around Z axis
            matrix = np.array([[c, -s, 0, 0],
                               [s, c, 0, 0],
                               [0, 0, 1, 0],
                               [0, 0, 0, 1]])
            surface.rotate(center, matrix)


class Object:
    def __init__(self):
        self.nodes = np.ones((0, 4))

    def addNodes(self, node_array):
        ones_column = np.ones((len(node_array), 1))
        ones_added = np.hstack((node_array, ones_column))
        self.nodes = np.vstack((self.nodes, ones_added))

    def findCenter(self):
        mean = self.nodes.mean(axis=0)
        return mean

    def rotate(self, center, matrix):
        for i, node in enumerate(self.nodes):
            self.nodes[i] = center + np.matmul(matrix, node - center)


xyz = []

for i in range(MAP_HEIGHT + 1):
    lat = (pi / MAP_HEIGHT) * i  #finally found reason image was wrogly displayed i have put "+" instead of "*"
    for j in range(MAP_WIDTH + 1):
        lon = (2 * pi / MAP_WIDTH) * j
        x = round(R * sin(lat) * cos(lon), 2)
        y = round(R * sin(lat) * sin(lon), 2)
        z = round(R * cos(lat), 2)
        xyz.append((x, y, z))

xyz_moon = []

for i in range(MAP_MOON_HEIGHT + 1):
    lat = (pi / MAP_MOON_HEIGHT) * i  #finally found reason image was wrogly displayed i have put "+" instead of "*"
    for j in range(MAP_MOON_WIDTH + 1):
        lon = (2 * pi / MAP_MOON_WIDTH) * j
        x = round(R_of_moon * sin(lat) * cos(lon), 2)
        y = round(R_of_moon * sin(lat) * sin(lon), 2)
        z = round(R_of_moon * cos(lat), 2)
        xyz_moon.append((x, y, z))

spin = 0.01
running = True

pv = Projection(WIDTH, HEIGHT)
earth = Object()
moon = Object()
earth_nodes = [i for i in xyz]
moon_nodes = [i for i in xyz_moon]
earth.addNodes(np.array(earth_nodes))
moon.addNodes(np.array(moon_nodes))
pv.addSurface('earth', earth)
pv.addSurface('moon', moon)
pv.display()

while running:
    dt = clock.tick(FPS)/1000.0

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    cs = np.cos(spin)
    ss = np.sin(spin)
    pv.screen.fill(pv.background)
    earth.rotate(earth.findCenter(), np.array([[cs, -ss, 0, 0],
                                               [ss, cs, 0, 0],
                                               [0, 0, 1, 0],
                                               [0, 0, 0, 1]]))
    pv.display()

    pg.display.update()
    # spin += 0.01 * dt
