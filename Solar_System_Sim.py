import pygame
import math
import keyboard

WIDTH, HEIGHT = 1350, 650
BLACK = (0, 0, 0)
S_YELLOW = (255, 223, 34)
CenterPosx = (WIDTH/2)
CenterPosy = (HEIGHT/2)

AU = 1.496e11  # Astronomical Unit in meters
G = 6.67430e-11 # Gravitational constant
SCALE1 = 250/AU # Scale for rendering planets




pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))


def clamp(n, min, max):
    if n < min:
        return int(min)
    elif n > max:
        return int(max)
    else:
        return int(n)

class Body:
    def __init__(self, name, mass, radius, color, posX, posY):
        self.name = name
        self.mass = mass
        
        self.radius = radius
        self.color = color
        self.posX = float(posX)
        self.posY = float(posY)
        self.velX = 0
        self.velY = 0
        
        
        
    def render(self):
        # Convert position (meters → pixels)
        x = self.posX * SCALE1 + WIDTH / 2
        y = self.posY * SCALE1 + HEIGHT / 2

        # DO NOT modify self.radius
        radius = self.radius * SCALE1
        radius = radius * 10

        # Safety checks
        if math.isnan(radius) or math.isinf(radius):
            return

        if radius <= 0:
            return
        

        pygame.draw.circle(
            screen,
            self.color,
            (int(x), int(y)),
            int(clamp(radius, 2, 200))
        )
# SIIIIIXXXXX SEVEEEEEENNNNNN


    def gravitationalAttraction(self, other):
        # print(self.radius, self.posX, self.posY)
        other_posX = other.posX
        other_posY = other.posY
        distanceToOtherX= other_posX - self.posX
        distanceToOtherY= other_posY - self.posY
        
        distance = math.sqrt(distanceToOtherX**2 + distanceToOtherY**2)
        
        if distance == 0:
            return 0, 0

    
        forceAttraction = G*(self.mass * other.mass) / (distance**2)
        theta = math.atan2(distanceToOtherY, distanceToOtherX)
        forceX = math.cos(theta) * forceAttraction
        forceY = math.sin(theta) * forceAttraction
        return forceX, forceY
    
    def updatePosition(self, bodies):
        if not keyboard.is_pressed('space'):
            
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
    
    
    def Simulate(self, bodies):
        self.updatePosition(bodies)
        self.render()
    


def PsuedoSolarSystem():
    Sun.Simulate(bodies)
    Earth.Simulate(bodies)
    Mars.Simulate(bodies)
    Mercury.Simulate(bodies)
    Venus.Simulate(bodies)
    Jupiter.Simulate(bodies)


def BinaryStarSystem():
    StarB.velY = 40000
    StarA.Simulate(bodies2)
    StarB.Simulate(bodies2)
    X1Planet.Simulate(bodies2)
    

def main(): 
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)
        
        #Stuff happens here
        
        PsuedoSolarSystem()
        # BinaryStarSystem()   
        
        # print(math.sqrt(Earth.posX**2 + Earth.posY**2))
        pygame.display.set_caption("Solar System Simulation")
        pygame.display.flip()



#Some cool bodies with actual real data
Sun = Body("Sun", 1.9891e30, 696340e3, S_YELLOW, 0, 0)
Earth = Body("Earth", 5.972e24, 6371e3, (0, 0, 255), AU, 0)
Earth.velY = -29780
Mars = Body("Mars", 6.39e23, 3389.5e3, (255, 0, 0), 1.524 * AU, 0)
Mars.velY = -24070
Mercury = Body("Mercury", 3.285e23, 2439.7e3, (128, 128, 128), 0.387 * AU, 0)
Mercury.velY = -47360
Venus = Body("Venus", 4.867e24, 6051.8e3, (255, 165, 0), 0.723 * AU, 0)
Venus.velY = -35020
Jupiter = Body("Jupiter", 1.898e27, 69911e3, (255, 215, 0), 5.204 * AU, 0)
Jupiter.velY = -13070

#Not so real data, but still fun to watch :D
StarA = Body("StarA", 2e30, 700000e3, (255, 255, 255), -0.2 * AU, -AU*1.2)
StarB = Body("StarB", 2e30, 700000e3, (255, 255, 255), 0.2 * AU, -AU*1.2)
X1Planet = Body("X1Planet", 5e26, 70005e3, (0, 255, 255), AU, 0)


#Lists of bodies per simulation(or solar systems idk)
bodies = [Sun, Earth, Mars, Mercury, Venus, Jupiter]
bodies2 = [StarA, StarB, X1Planet]



main()
