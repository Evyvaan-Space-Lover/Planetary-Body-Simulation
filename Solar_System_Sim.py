import pygame
import math

WIDTH, HEIGHT = 1350, 650
BLACK = (0, 0, 0)
S_YELLOW = (255, 223, 34)
CenterPosx = (WIDTH/2)
CenterPosy = (HEIGHT/2)

AU = 149597870700  # Astronomical Unit in meters
G = 6.67430e-11  # Gravitational constant
SCALE1 = 6000 # Scale for rendering planets
SCALEG = 6e8 # Scale for calculating gravitational attraction



pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))


class Body:
    def __init__(self, name, mass, radius, color, posX, posY):
        self.name = name
        self.mass = mass
        self.radius = radius/SCALE1
        self.color = color
        self.posX = posX
        self.posY = posY
        
    def render(self):
        pygame.draw.circle(screen, self.color, (int(self.posX), int(self.posY)), float(self.radius))


def main(): 
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)
        #Stuff happens here
        Sun.render()
        Earth.render()

        pygame.display.set_caption("Solar System Simulation")
        pygame.display.flip()


Sun = Body("Sun", 1.9891e30, 695700, S_YELLOW, CenterPosx, CenterPosy)
Earth = Body("Earth", 5.972e24, 6371, (0, 0, 255), CenterPosx + (AU/SCALEG) + Sun.radius, CenterPosy)

main()