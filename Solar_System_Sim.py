#Fully Made by Evyvaan, with a little help from the internet for the trails, physics and data, but it works so be it
#Project started on 17 March 2025

import pygame
pygame.init()
import math

WIDTH, HEIGHT = 1350, 650

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
S_YELLOW = (255, 223, 34)

CenterPosx = (WIDTH/2)
CenterPosy = (HEIGHT/2)

AU = 1.496e11  # Astronomical Unit in meters
G = 6.67430e-11 # Gravitational constant
SCALE1 = 250/AU # Scale for rendering planets

bodies = []
TRAIL_LENGTH = 500

pygame.display.set_caption("Solar System Simulation")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

def removeFromList(item):
    if item in bodies:
        bodies.remove(item)

def clamp(n, min, max):
    if n < min:
        return int(min)
    elif n > max:
        return int(max)
    else:
        return int(n)
    
def NewRadii(R1, R2):
    FinalRadii = math.pow(R1**3 + R2**3, 1/3)
    return FinalRadii

class Body:
    def __init__(self, name, mass, radius, color, posX, posY):
        self.name = name
        self.mass = mass
        
        self.trail = []
        self.radius = radius
        self.color = color
        self.posX = float(posX)
        self.posY = float(posY)
        self.velX = 0
        self.velY = 0
        self.exists = True
        self.counter = 0
        self.lastposX = None
        self.lastposY = None
        self.CelestialBody = True


    def addToList(item):
        if item.counter == 0:
            bodies.append(item)
            item.counter = 1
        

    def render(self):
        if self.exists == True: 
        # Converting position (meters to pixels)
            x = self.posX * SCALE1 + CenterPosx
            y = self.posY * SCALE1 + CenterPosy

            # DO NOT modify self.radius
            radius = self.radius * SCALE1
            radius = radius * 10

            # Safety checks
            if math.isnan(radius) or math.isinf(radius):
                return

            if radius <= 0:
                return

            if math.isnan(x) or math.isinf(x) or math.isnan(y) or math.isinf(y):
                return

            # ngl, this is the only thing that i blatantly stole from the INTERNET cuz i had no idea how to do trails, and it works pretty well
            self.trail.append((int(x), int(y)))
            if len(self.trail) > TRAIL_LENGTH and not pygame.key.get_pressed()[pygame.K_SPACE]:
                self.trail.pop(0)
            
            if pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_s] or pygame.key.get_pressed()[pygame.K_r]: # dont make trail wihile zooming in or out bruh
                self.trail.clear()


            pygame.draw.circle(
                screen,
                self.color,
                (int(x), int(y)),
                int(clamp(radius, 3, 2000))
            )
            
            for a, b in zip(self.trail, self.trail[1:]):
                pygame.draw.aaline(screen, self.color, a, b, 2)



    def gravitationalAttraction(self, other):
        # print(self.radius, self.posX, self.posY)
        other_posX = other.posX
        other_posY = other.posY
        distanceToOtherX= other_posX - self.posX
        distanceToOtherY= other_posY - self.posY
        
        distance = math.hypot(distanceToOtherX, distanceToOtherY)
        
        if distance == 0:
            return 0, 0

    
        forceAttraction = G*(self.mass * other.mass) / (distance**2)
        theta = math.atan2(distanceToOtherY, distanceToOtherX)
        forceX = math.cos(theta) * forceAttraction
        forceY = math.sin(theta) * forceAttraction
        return forceX, forceY
    
    def updatePosition(self):
        if self.exists == True:
            totalForceX = 0
            totalForceY = 0
            for body in bodies:
                if body.name != self.name:
                    forceX, forceY = self.gravitationalAttraction(body)
                    totalForceX += forceX
                    totalForceY += forceY
                    
                    
            ax = totalForceX / self.mass
            ay = totalForceY / self.mass
            
            dt = 60 * 60 # Time step
            
            self.velX += ax * dt
            self.velY += ay * dt

            self.posX += self.velX * dt
            self.posY += self.velY * dt

    def merge(self, CollidedBody):
        if CollidedBody.mass < self.mass:
            self.mass += CollidedBody.mass
            self.radius = NewRadii(self.radius, CollidedBody.radius)
            CollidedBody.exists = False
            removeFromList(CollidedBody)
            self.velX = (self.velX * self.mass + CollidedBody.velX * CollidedBody.mass) / self.mass
            self.velY = (self.velY * self.mass + CollidedBody.velY * CollidedBody.mass) / self.mass


    def collideAndMerge(self):
        if self.exists == True:
            
            for body in bodies:
                if body.name != self.name:
                    other_posX = body.posX
                    other_posY = body.posY
                    distanceToOtherX= other_posX - self.posX
                    distanceToOtherY= other_posY - self.posY
                    
                    Sradius = self.radius
                    bradius = body.radius
                    
                    sphereHit = Sradius + bradius 
                    
                    distance1 = math.hypot(distanceToOtherY, distanceToOtherX)
                    
                    
                    if distance1 < sphereHit:
                        self.merge(body)
                        # print(f"{self.name} collided with {body.name}!")
                        # print(bodies)

    def trail(self, lastpos, currentpos):
        pygame.draw.line(screen, self.color, lastpos, currentpos, 1)

    def Simulate(self, paused=False):
        self.addToList()
        if not paused and self.exists == True:
            self.updatePosition()
            self.collideAndMerge()
        self.render()



def PsuedoSolarSystem(paused=False):
    Sun.Simulate(paused)
    Earth.Simulate(paused)
    Mars.Simulate(paused)
    Mercury.Simulate(paused)
    Venus.Simulate(paused)
    Jupiter.Simulate(paused)


def BinaryStarSystem(paused=False):
    StarA.Simulate(paused)
    StarB.Simulate(paused)
    X1Planet.Simulate(paused)


def testSystem(paused=False):
    bodyA.Simulate(paused)
    bodyB.Simulate(paused)


def elipticalOrbitSystem(paused=False):
    Star1.Simulate(paused)
    bodyC.Simulate(paused)

def main(): 
    global SCALE1
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(BLACK)
        Keys= pygame.key.get_pressed()
        
        
        #Stuff happens here
        
        # PsuedoSolarSystem(Keys[pygame.K_SPACE])
        # BinaryStarSystem(Keys[pygame.K_SPACE])
        testSystem(Keys[pygame.K_SPACE])
        # elipticalOrbitSystem(Keys[pygame.K_SPACE])

        # SagBlackhole.Simulate(Keys[pygame.K_SPACE])
        
        
        
        if Keys[pygame.K_w]:
            SCALE1 *= 1.001
        if Keys[pygame.K_s]:
            SCALE1 /= 1.001
        if Keys[pygame.K_r]:
            SCALE1 = 250/AU
        # print(math.sqrt(Earth.posX**2 + Earth.posY**2))
        pygame.display.flip()
    
    pygame.quit()



#Some cool bodies with actual real data
Sun = Body("Sun", 1.9891e30, 696340e3, S_YELLOW, 0, 0)
Earth = Body("Earth", 5.972e24, 6371e3, BLUE, AU, 0)
Earth.velY = -29780
Mars = Body("Mars", 6.39e23, 3389.5e3, RED, 1.524 * AU, 0)
Mars.velY = -24070
Mercury = Body("Mercury", 3.285e23, 2439.7e3, GREY, 0.387 * AU, 0)
Mercury.velY = -47360
Venus = Body("Venus", 4.867e24, 6051.8e3, ORANGE, 0.723 * AU, 0)
Venus.velY = -35020
Jupiter = Body("Jupiter", 1.898e27, 69911e3, YELLOW, 5.204 * AU, 0)
Jupiter.velY = -13070

#Not so real data, but still fun to watch :D
StarA = Body("StarA", 2e30, 700000e3, YELLOW, AU * 2.3, -0.4 * AU)
StarB = Body("StarB", 2e30, 700000e3, WHITE, AU * 2.3, 0.4 * AU)
X1Planet = Body("X1Planet", 5e26, 70005e3, CYAN, AU * 2, AU)
StarA.velX = -10000 
StarB.velX = -40000
X1Planet.velY = -20000
bodyA = Body("BodyA", 1e30, 5000e5, RED, -AU*0.2, 0)
bodyB = Body("BodyB", 1e20, 5000e5, GREY, AU*0.2, 0)
Star1 = Body("Star1", 10e30, 10000e5, RED, -AU, 0)
bodyC = Body("BodyC", 1e24, 5000e2, GREY, AU*0.6, 0)
bodyC.velY = -18000

SagBlackhole = Body("SagBlackhole", 4.3e6 * Sun.mass, 31.6 * Sun.radius, GREY, 0, 0) #Sagittarius A* is the supermassive black hole at the center of our galaxy, with a mass of about 4.3 million times that of the Sun and an estimated radius of around 31.6 times the Sun's radius.



main()