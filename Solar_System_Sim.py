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
SYSTEM = None

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

def CamControls():
    global CenterPosx
    global CenterPosy
    global SCALE1
    Keys= pygame.key.get_pressed()
    if Keys[pygame.K_t]: # this controller sucks bruh
        CenterPosy *= 1.0015
    if Keys[pygame.K_g]:
        CenterPosy /= 1.0015
    if Keys[pygame.K_f]:
        CenterPosx *= 1.0015
    if Keys[pygame.K_h]:
        CenterPosx /= 1.0015
    if Keys[pygame.K_w]:
        SCALE1 *= 1.001
    if Keys[pygame.K_s]:
        SCALE1 /= 1.001
    if Keys[pygame.K_r]:
        SCALE1 = 250/AU

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
        self.prevPosX = None
        self.prevPosY = None
        self.lastposX = None
        self.lastposY = None
        self.CelestialBody = True
        self.CenterPosX= None
        self.CenterPosY = None

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
            if not math.isfinite(radius) or radius <= 0:
                return

            if not (math.isfinite(x) and math.isfinite(y)):
                return

            # ngl, this is the only thing that i blatantly stole from the INTERNET cuz i had no idea how to do trails, and it works pretty well
            self.trail.append((int(x), int(y)))
            if len(self.trail) > TRAIL_LENGTH and not pygame.key.get_pressed()[pygame.K_SPACE]:
                self.trail.pop(0)
            
            if pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_s] or pygame.key.get_pressed()[pygame.K_r] or pygame.key.get_pressed()[pygame.K_t] or pygame.key.get_pressed()[pygame.K_g] or pygame.key.get_pressed()[pygame.K_f] or pygame.key.get_pressed()[pygame.K_h]: # dont make trail wihile zooming in or out and movng bruh
                self.trail.clear()
            
            
            pygame.draw.circle(
                screen,
                self.color,
                (int(x), int(y)),
                int(clamp(radius, 5, 200))
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
            
            # Initialize previous position for Verlet integration if not set
            if self.prevPosX is None:
                self.prevPosX = self.posX - self.velX * dt
                self.prevPosY = self.posY - self.velY * dt
            
            #Verlet integration for better accuracy and stability, especially with larger time steps
            newPosX = 2 * self.posX - self.prevPosX + ax * dt ** 2
            newPosY = 2 * self.posY - self.prevPosY + ay * dt ** 2
            
            self.prevPosX = self.posX
            self.prevPosY = self.posY
            self.posX = newPosX
            self.posY = newPosY
            
            
            

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



def SolarSystem(paused=False):
    Sun.Simulate(paused)
    # Moon.Simulate(paused)
    Earth.Simulate(paused)
    Mars.Simulate(paused)
    Mercury.Simulate(paused)
    Venus.Simulate(paused)
    Jupiter.Simulate(paused)


def BinaryStarSystem(paused=False):
    StarA.Simulate(paused)
    StarB.Simulate(paused)
    X1Planet.Simulate(paused)

def elipticalOrbitSystem(paused=False):
    Star1.Simulate(paused)
    bodyC.Simulate(paused)
    
def LagrangianPointDemoSystem(paused=False):
    pygame.draw.line(screen, WHITE, (Earth.posX * SCALE1 + CenterPosx, Earth.posY * SCALE1 + CenterPosy), (Sun.posX * SCALE1 + CenterPosx, Sun.posY* SCALE1 + CenterPosy), 1)
    pygame.draw.line(screen, WHITE, (Earth.posX * SCALE1 + CenterPosx, Earth.posY * SCALE1 + CenterPosy), (LagrangePoint4Asteroid.posX * SCALE1 + CenterPosx, LagrangePoint4Asteroid.posY * SCALE1 + CenterPosy), 1)
    pygame.draw.line(screen, WHITE, (Sun.posX * SCALE1 + CenterPosx, Sun.posY * SCALE1 + CenterPosy), (LagrangePoint4Asteroid.posX * SCALE1 + CenterPosx, LagrangePoint4Asteroid.posY * SCALE1 + CenterPosy), 1)
    
    pygame.draw.line(screen, WHITE, (Earth.posX * SCALE1 + CenterPosx, Earth.posY * SCALE1 + CenterPosy), (LagrangePoint5Asteroid.posX * SCALE1 + CenterPosx, LagrangePoint5Asteroid.posY * SCALE1 + CenterPosy), 1)
    pygame.draw.line(screen, WHITE, (Sun.posX * SCALE1 + CenterPosx, Sun.posY * SCALE1 + CenterPosy), (LagrangePoint5Asteroid.posX * SCALE1 + CenterPosx, LagrangePoint5Asteroid.posY * SCALE1 + CenterPosy), 1)
    pygame.draw.line(screen, WHITE, (LagrangePoint4Asteroid.posX * SCALE1 + CenterPosx, LagrangePoint4Asteroid.posY * SCALE1 + CenterPosy), (LagrangePoint5Asteroid.posX * SCALE1 + CenterPosx, LagrangePoint5Asteroid.posY* SCALE1 + CenterPosy), 1)
    Sun.Simulate(paused)
    Earth.Simulate(paused)
    LagrangePoint4Asteroid.Simulate(paused)
    LagrangePoint5Asteroid.Simulate(paused)


def Sim(System):
    Keys= pygame.key.get_pressed()
    if System == "SolarSystem":
        SolarSystem(Keys[pygame.K_SPACE])
    if System == "BinarySystem":
        BinaryStarSystem(Keys[pygame.K_SPACE])
    if System =="ElipticalSystem":
        elipticalOrbitSystem(Keys[pygame.K_SPACE])
    if System == "L4 and L5":
        LagrangianPointDemoSystem(Keys[pygame.K_SPACE])

def mainSIM(System): 
    global SCALE1 # I have no idea why i have to do this but if i dont do this, it falls apart lmao
    global CenterPosx
    global CenterPosy
    global SYSTEM
    running = True
    bodies.clear()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(BLACK)
        Keys= pygame.key.get_pressed()
        CamControls()
        
        Sim(System)
        
        # print(math.sqrt(Earth.posX**2 + Earth.posY**2))
        pygame.display.flip()
    




#Some cool bodies with actual real data
Sun = Body("Sun", 1.9891e30, 696340e3, S_YELLOW, 0, 0)
Earth = Body("Earth", 5.972e24, 6371e3, BLUE, AU, 0)
Earth.velY = -29780
Moon = Body("Moon", 7.34767309e22, 1737.4e3, WHITE, 1.0026 * AU, 0)
Moon.velY = -30780
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
bodyC = Body("BodyC", 1e25, 5000e2, GREY, AU*0.6, 0)
bodyC.velY = -18000

# Demonstrating Lagrangian Points, with an asteroid placed at L4
L4x = AU * 0.5
L4y = -AU * math.sqrt(3)/2
L5y = AU * math.sqrt(3)/2
LagrangePoint4Asteroid = Body("Asteroid 1", 2e20, 3e3, GREY, L4x, L4y)
LagrangePoint5Asteroid = Body("Asteroid 2", 2e20, 3e3, GREY, L4x, L5y)

r = math.sqrt(L4x**2 + L4y**2)
v = math.sqrt(G * Sun.mass / r)

# perpendicular direction
LagrangePoint4Asteroid.velX = L4y / r * v
LagrangePoint4Asteroid.velY = -L4x / r * v #negative, as in my sim, its topsy turvy in terms of co-ordinates
LagrangePoint5Asteroid.velX = -L4y / r * v
LagrangePoint5Asteroid.velY = -L4x / r * v #negative, as in my sim, its topsy turvy in terms of co-ordinates

SagBlackhole = Body("SagBlackhole", 4.3e6 * Sun.mass, 31.6 * Sun.radius, GREY, 0, 0) #Sagittarius A* is the supermassive black hole at the center of our galaxy, with a mass of about 4.3 million times that of the Sun and an estimated radius of around 31.6 times the Sun's radius.


def MAIN():
    running = True
    print("========================================EvyvaanSingh========================================")
    print("\nWelcome To 'Planetary Body Simulation' ! ")
    print("\n Please Choose the desired system to simulate or enter commands. \n Our Solar System (1) \n Binary Star System (2) \n System in which the the satellite planet follows an Eliptical Path (3) \n Demonstration of simulation of bodies in L4 AND L5 points (4)")
    while running:
        choose = input(">>> ")
        if choose == "1":
            print("Task Started Successfully! \n Please restart the program to run another simulation or command by entering 'exit'.")
            mainSIM("SolarSystem")
        elif choose == "2":
            print("Task Started Successfully! \n Please restart the program to run another simulation or command by entering 'exit'.")
            mainSIM("BinarySystem")
        elif choose == "3":
            print("Task Started Successfully! \n Please restart the program to run another simulation or command by entering 'exit'.")
            mainSIM("ElipticalSystem")
        elif choose == "4":
            print("Task Started Successfully! \n Please restart the program to run another simulation or command by entering 'exit'.")
            mainSIM("L4 and L5")
        elif choose == "exit":
            running = False
        else:
            print("Invalid Command")


MAIN()