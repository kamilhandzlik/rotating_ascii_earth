import pygame as pg
import numpy as np
from math import pi, sin, cos

clock = pg.time.Clock()
FPS = 30

WIDTH = 800
HEIGHT = 800

R = 250
MAP_WIDTH = 101
MAP_HEIGHT = 31

pg.init()

my_font = pg.font.SysFont('arial', 14)

with open('image.txt', 'r') as file:
    data = [line.strip() for line in file.readlines()]

ascii_chars = []
for line in data:
    for char in line:
        ascii_chars.append(char)

inverted_ascii_chars = ascii_chars[::-1]


class Projection:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pg.display.set_mode((width, height))
        self.background = (10, 10, 60)
        pg.display.set_caption('ASCII 3D EARTH')
        self.surfaces = {}

    def addSurface(self, name, surface):
        self.surfaces[name] = surface

    def display(self):
        self.screen.fill(self.background)

        for surface in self.surfaces.values():
            i = 0
            for node in surface.nodes:
                if node[1] > 0:
                    x, y = int(WIDTH / 2 + node[0]), int(HEIGHT / 2 + node[2])
                    char_index = int((y % HEIGHT) * WIDTH + x) % len(inverted_ascii_chars)
                    self.text = inverted_ascii_chars[char_index]
                    self.text_surface = my_font.render(self.text, False, (0, 255, 0))
                    self.screen.blit(self.text_surface, (x, y))
                i += 1

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

            # Update the screen coordinates after rotation
            rotated_nodes = []
            for node in surface.nodes:
                rotated_node = center + np.matmul(matrix, node - center)
                rotated_nodes.append(rotated_node)

            surface.nodes = np.array(rotated_nodes)


class Object:
    def __init__(self):
        self.nodes = np.zeros((0, 4))

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
    lat = (pi / MAP_HEIGHT) + i
    for j in range(MAP_WIDTH + 1):
        lon = (2 * pi / MAP_WIDTH) * j
        x = round(R * sin(lat) * cos(lon), 2)
        y = round(R * sin(lat) * sin(lon), 2)
        z = round(R * cos(lat), 2)
        xyz.append((x, y, z))

spin = 0
running = True

pv = Projection(WIDTH, HEIGHT)
globe = Object()
globe_nodes = [i for i in xyz]
globe.addNodes(np.array(globe_nodes))
pv.addSurface('globe', globe)

while running:
    clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    pv.screen.fill(pv.background)
    globe.rotateAll(spin)
    pv.display()

    pg.display.update()
    spin += 0.05
