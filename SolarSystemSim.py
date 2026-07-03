#Fully Made by Evyvaan, with a little help from the internet for the trails, physics and data, but it works so be it
#Project started on 17 March 2025

from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import pygame_widgets
import pygame
import tkinter as tk
from tkinter import ttk, simpledialog
pygame.init()
import math
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import os
import sys
import subprocess

import random

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
TIMESTEP = 60 * 60

bodies = []
plotBodies = []
TRAIL_LENGTH = 500
SYSTEM = None
PLTORNOT = False
TYPEPLT = None
TOTAL_PE = []
TOTAL_KE = []
TOTAL_E = []

SHOW_TRAIL = True
SHOW_ENERGY = False
PLTVELOCITY = False
LINE2COM = False

def restart():
    script_path = os.path.abspath(__file__)
    
    python = sys.executable
    subprocess.Popen([python, script_path])
    sys.exit()
    print("'Bye'  -  Evyvaan said calmly")
    print("================================================================================================================================")

def removeFromList(item):
    if item in bodies:
        bodies.remove(item)

def graphCOM(bodies):
    plt.figure()
    for body in bodies:
        plt.plot(body.DISTANCECOM, label=f"{body.name} Distance to COM")
    plt.legend()
    plt.title("Distance to Center of Mass vs Time")
    plt.xlabel("Frames")
    plt.ylabel("Distance to COM (in meters)")
    plt.show()

def graphVelocity(bodies):
    plt.figure()
    for body in bodies:
        plt.plot(body.VELOCITY, label=f"{body.name} Velocity")
    plt.legend()
    plt.title("Velocity vs Time")
    plt.xlabel("Frames")
    plt.ylabel("Velocity (in m/s)")
    plt.show()

def graphPosition(bodies):
    plt.figure()
    for body in bodies:
        x = body.X
        y = [-val for val in body.Y]
        plt.plot(x, y, label=f"{body.name} Trajectory")
    plt.legend()
    plt.title("Trajectory (X vs Y)")
    plt.xlabel("X Trajectory (in meters)")
    plt.ylabel("Y Trajectory (in meters)")
    plt.show()


def graphPosition3D(bodies):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for body in bodies:
        x = body.X
        y = [-val for val in body.Y]
        time = range(len(x))
        name = body.name
        ax.plot(x, y, time, label=f"{name} Path")
    ax.set_title("3D Trajectory (X vs Y vs Time)")
    ax.set_xlabel("X Position (in meters)")
    ax.set_ylabel("Y Position (in meters)")
    ax.set_zlabel("Time (in seconds)")
    ax.legend()
    ax.view_init(elev=30, azim=120)
    plt.show()



def graphEnergies(data, data1, data2):
    plt.figure()
    plt.plot(data, label="Total Energy Of the System")
    plt.plot(data1, label="Total Kinetic Energy of the System")
    plt.plot(data2, label="Total Potential Energy of the System")
    plt.legend()
    plt.title("Energy vs Time")
    plt.xlabel("Frames")
    plt.ylabel("Energy (In Joules)")
    plt.show()

def clamp(n, min, max):
    if n < min:
        return int(min)
    elif n > max:
        return int(max)
    else:
        return int(n)

def printASCII():
    print("""                                                                    ..;===+.
                                                                .:=iiiiii=+=
                                                             .=i))=;::+)i=+,
                                                          ,=i);)I)))I):=i=;
                                                       .=i==))))ii)))I:i++
                                                     +)+))iiiiiiii))I=i+:'
                                .,:;;++++++;:,.       )iii+:::;iii))+i='
                             .:;++=iiiiiiiiii=++;.    =::,,,:::=i));=+'
                           ,;+==ii)))))))))))ii==+;,      ,,,:=i))+=:
                         ,;+=ii))))))IIIIII))))ii===;.    ,,:=i)=i+
                        ;+=ii)))IIIIITIIIIII))))iiii=+,   ,:=));=,
                      ,+=i))IIIIIITTTTTITIIIIII)))I)i=+,,:+i)=i+
                     ,+i))IIIIIITTTTTTTTTTTTI))IIII))i=::i))i='
                    ,=i))IIIIITLLTTTTTTTTTTIITTTTIII)+;+i)+i`
                    =i))IIITTLTLTTTTTTTTTIITTLLTTTII+:i)ii:'
                   +i))IITTTLLLTTTTTTTTTTTTLLLTTTT+:i)))=,
                   =))ITTTTTTTTTTTLTTTTTTLLLLLLTi:=)IIiii;
                  .i)IIITTTTTTTTLTTTITLLLLLLLT);=)I)))))i;
                  :))IIITTTTTLTTTTTTLLHLLLLL);=)II)IIIIi=:
                  :i)IIITTTTTTTTTLLLHLLHLL)+=)II)ITTTI)i=
                  .i)IIITTTTITTLLLHHLLLL);=)II)ITTTTII)i+
                  =i)IIIIIITTLLLLLLHLL=:i)II)TTTTTTIII)i'
                +i)i)))IITTLLLLLLLLT=:i)II)TTTTLTTIII)i;
              +ii)i:)IITTLLTLLLLT=;+i)I)ITTTTLTTTII))i;
             =;)i=:,=)ITTTTLTTI=:i))I)TTTLLLTTTTTII)i;
           +i)ii::,  +)IIITI+:+i)I))TTTTLLTTTTTII))=,
         :=;)i=:,,    ,i++::i))I)ITTTTTTTTTTIIII)=+'
       .+ii)i=::,,   ,,::=i)))iIITTTTTTTTIIIII)=+
      ,==)ii=;:,,,,:::=ii)i)iIIIITIIITIIII))i+:'
     +=:))i==;:::;=iii)+)=  `:i)))IIIII)ii+'
   .+=:))iiiiiiii)))+ii;
  .+=;))iiiiii)));ii+
 .+=i:)))))))=+ii+
.;==i+::::=)i=;
,+==iiiiii+,
`+=+++;`
""")

def askPlotter():
    if input("Do you want to plot some niffty data? (y/n) \n > ").lower() == "y":
        answer = input("What do you wanna plot? \n -Velocities (1) \n -Total energy of the system (2) \n -Distance to the Center of Mass (3) \n -Record Trajectory (4) \n -Record Position with Time (5) \n -All of the above (6) \n  > ")
        if answer == "1":
            return True, "Velocity"
        elif answer == "2":
            return True, "Energy"
        elif answer == "3":
            return True, "COM"
        elif answer == "4":
            return True, "Position"
        elif answer == "5":
            return True, "Position3D"
        elif answer == "6":
            return True, "all"
        else:
            print("Proceeding with No plots")
            return False, None
    else:
        return False, None

def askPlotterGUI():
    root = tk.Tk()
    root.withdraw()

    options = [
        "Velocity",
        "Energy",
        "COM",
        "Position",
        "Position3D",
        "all"
    ]
    option_text = "\n".join([
        "1 - Velocities",
        "2 - Total energy of the system",
        "3 - Distance to the Center of Mass",
        "4 - Record Trajectory",
        "5 - Record Position with Time",
        "6 - All of the above"
    ])

    answer = simpledialog.askstring(
        "Plotting Options",
        f"Choose the plot type:\n{option_text}",
        parent=root
    )

    root.destroy()
    if not answer:
        return False, None

    answer = answer.strip()
    if answer == "1":
        return True, "Velocity"
    if answer == "2":
        return True, "Energy"
    if answer == "3":
        return True, "COM"
    if answer == "4":
        return True, "Position"
    if answer == "5":
        return True, "Position3D"
    if answer == "6":
        return True, "all"

    return False, None

def calcVelocity(body):
    vx = (body.posX - body.prevPosX) / TIMESTEP
    vy =(body. posY - body.prevPosY) / TIMESTEP
    
    velocity = math.hypot(vx, vy)
    return vx, vy, velocity

def calcCenterOfMass():
    total_mass = sum(body.mass for body in bodies if body.exists)
    if total_mass == 0:
        return 0.0, 0.0

    com_x = sum(body.mass * body.posX for body in bodies if body.exists) / total_mass
    com_y = sum(body.mass * body.posY for body in bodies if body.exists) / total_mass
    return com_x, com_y

def calcEnergy():
    KE = 0
    for b in bodies:
        vx, vy, velocity = calcVelocity(b)
        KE += 1/2 * b.mass * velocity**2
    
    PE = 0
    for i in range(len(bodies)):
        for j in range(i+1, len(bodies)):
            dx = bodies[j].posX - bodies[i].posX
            dy = bodies[j].posY - bodies[i].posY
            dis = math.hypot(dx, dy)
            if dis != 0:
                PE -= G * bodies[i].mass * bodies[j].mass / dis
    E = KE + PE # Total energy in the system
    return E, KE, PE

def NewRadii(R1, R2):
    FinalRadii = math.pow(R1**3 + R2**3, 1/3)
    return FinalRadii

def TimestepControls():
    global TIMESTEP
    Keys= pygame.key.get_pressed()
    if Keys[pygame.K_q]:
        TIMESTEP *= 1.1
    if Keys[pygame.K_e]:
        TIMESTEP /= 1.1

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
        self.CenterPosX= None
        self.CenterPosY = None
        self.distanceToCOM = None
        
        self.DISTANCECOM = []
        self.VELOCITY = []
        self.X = []
        self.Y = []
        self.velocity = 0

    def addToList(item):
        global plotBodies
        if item not in bodies:
            bodies.append(item)
        if item not in plotBodies:
            plotBodies.append(item)
        if item.counter == 0:
            item.counter = 1


    def render(self, screen, trail):
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

            if LINE2COM:
                comX, comY = calcCenterOfMass()
                comX = comX * SCALE1 + CenterPosx
                comY = comY * SCALE1 + CenterPosy
                pygame.draw.line(screen, WHITE, (x, y), (comX, comY), 1)

            # ngl, this is the only thing that i blatantly stole from the INTERNET cuz i had no idea how to do trails, and it works pretty well
            self.trail.append((int(x), int(y)))
            if len(self.trail) > trail and not pygame.key.get_pressed()[pygame.K_SPACE]:
                self.trail.pop(0)
            
            if pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_s] or pygame.key.get_pressed()[pygame.K_r] or pygame.key.get_pressed()[pygame.K_t] or pygame.key.get_pressed()[pygame.K_g] or pygame.key.get_pressed()[pygame.K_f] or pygame.key.get_pressed()[pygame.K_h]: # dont make trail wihile zooming in or out and movng bruh
                self.trail.clear()
            
            pygame.draw.circle(
                screen,
                self.color,
                (int(x), int(y)),
                int(clamp(radius, 5, 200))
            )
            if SHOW_TRAIL:
                for a, b in zip(self.trail, self.trail[1:]):
                    pygame.draw.aaline(screen, self.color, a, b, 2)




    def gravitationalAttraction(self, other):
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
    
    def updatePosition(self, dt):
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
            
            dt = dt # Time step
            
            # Initialize previous position for Verlet integration if not set
            if self.prevPosX is None:
                self.prevPosX = self.posX - self.velX * dt
                self.prevPosY = self.posY - self.velY * dt
            
            #Verlet integration for better accuracy and stability, especially with larger time steps
            newPosX = 2 * self.posX - self.prevPosX + ax * dt ** 2
            newPosY = 2 * self.posY - self.prevPosY + ay * dt ** 2
            
            self.velX, self.velY, self.velocity = calcVelocity(self)
            
            self.prevPosX = self.posX
            self.prevPosY = self.posY
            self.posX = newPosX
            self.posY = newPosY
            
            self.distanceToCOM = math.hypot(self.posX - comX, self.posY - comY)
            
            if PLTORNOT == True and TYPEPLT == "COM" or TYPEPLT == "all":
                self.DISTANCECOM.append(self.distanceToCOM)
            if PLTVELOCITY == True:
                self.VELOCITY.append(self.velocity)
            if PLTORNOT and TYPEPLT in ("Position", "Position3D", "all"):
                self.X.append(self.posX)
                self.Y.append(self.posY)

    def merge(self, CollidedBody):
        if CollidedBody.mass < self.mass:
            self.mass += CollidedBody.mass
            self.radius = NewRadii(self.radius, CollidedBody.radius)
            CollidedBody.exists = False
            removeFromList(CollidedBody)

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
                    
                    distance1 = math.sqrt(distanceToOtherX**2 + distanceToOtherY**2)
                    
                    if distance1 < sphereHit:
                        self.merge(body)

    def Simulate(self, screen, paused=False):
        global TIMESTEP
        global TRAIL_LENGTH
        self.addToList()
        if not paused and self.exists == True:
            self.updatePosition(TIMESTEP)
            self.collideAndMerge()
        self.render(screen, TRAIL_LENGTH)

def screenShot(screen):
    if pygame.key.get_pressed()[pygame.K_p]:
        filename=os.path.abspath(f"SimShot_{random.randint(1, 999)}.png")
        pygame.image.save(screen, filename)
        print(f"Saved to: {filename}")

def SolarSystem(screen, paused=False):
    Sun.Simulate(paused, screen)
    # Moon.Simulate(paused)
    Earth.Simulate(paused,screen)
    Mars.Simulate(paused, screen)
    Mercury.Simulate(paused, screen)
    Venus.Simulate(paused,screen)
    Jupiter.Simulate(paused, screen)
    Saturn.Simulate(paused, screen)
    Uranus.Simulate(paused, screen)
    Neptune.Simulate(paused, screen)
    
    screenShot(paused)

def BinaryStarSystem(screen, paused=False):
    StarA.Simulate(paused, screen)
    StarB.Simulate(paused, screen)
    X1Planet.Simulate(paused, screen)
    
    screenShot(paused)

def elipticalOrbitSystem(screen, paused=False):
    Star1.Simulate(paused, screen)
    bodyC.Simulate(paused, screen)
    
    screenShot(paused)

def LagrangianPointDemoSystem(screen, paused):
    #puased and screen variables are exchanged for some reason. im too exhausted to find why, but it works as it should so i really dont care
    pygame.draw.line(paused, WHITE, (Earth.posX * SCALE1 + CenterPosx, Earth.posY * SCALE1 + CenterPosy), (Sun.posX * SCALE1 + CenterPosx, Sun.posY* SCALE1 + CenterPosy), 1)
    pygame.draw.line(paused, WHITE, (Earth.posX * SCALE1 + CenterPosx, Earth.posY * SCALE1 + CenterPosy), (LagrangePoint4Asteroid.posX * SCALE1 + CenterPosx, LagrangePoint4Asteroid.posY * SCALE1 + CenterPosy), 1)
    pygame.draw.line(paused, WHITE, (Sun.posX * SCALE1 + CenterPosx, Sun.posY * SCALE1 + CenterPosy), (LagrangePoint4Asteroid.posX * SCALE1 + CenterPosx, LagrangePoint4Asteroid.posY * SCALE1 + CenterPosy), 1)
    
    pygame.draw.line(paused, WHITE, (Earth.posX * SCALE1 + CenterPosx, Earth.posY * SCALE1 + CenterPosy), (LagrangePoint5Asteroid.posX * SCALE1 + CenterPosx, LagrangePoint5Asteroid.posY * SCALE1 + CenterPosy), 1)
    pygame.draw.line(paused, WHITE, (Sun.posX * SCALE1 + CenterPosx, Sun.posY * SCALE1 + CenterPosy), (LagrangePoint5Asteroid.posX * SCALE1 + CenterPosx, LagrangePoint5Asteroid.posY * SCALE1 + CenterPosy), 1)
    pygame.draw.line(paused, WHITE, (LagrangePoint4Asteroid.posX * SCALE1 + CenterPosx, LagrangePoint4Asteroid.posY * SCALE1 + CenterPosy), (LagrangePoint5Asteroid.posX * SCALE1 + CenterPosx, LagrangePoint5Asteroid.posY* SCALE1 + CenterPosy), 1)
    Sun.Simulate(paused, screen)
    Earth.Simulate(paused, screen)
    LagrangePoint4Asteroid.Simulate(paused, screen)
    LagrangePoint5Asteroid.Simulate(paused, screen)
    
    screenShot(paused)

def ThreeBodyChaos(screen, paused=False):
    tbody1.Simulate(paused, screen)
    tbody2.Simulate(paused, screen)
    tbody3.Simulate(paused, screen)
    
    screenShot(paused)


def HorseShoeCrabSystem(screen, paused=False):
    Sun.Simulate(paused, screen)
    Earth.Simulate(paused, screen)
    obj.Simulate(paused, screen)
    
    screenShot(paused)

def SlingShot(screen, paused=False):
    ProbeA.Simulate(paused, screen)
    BigPlanetForSlingShot.Simulate(paused, screen)
    
    screenShot(paused)


def Sim(System, screen):
    Keys= pygame.key.get_pressed()
    if System == "SolarSystem":
        SolarSystem(Keys[pygame.K_SPACE], screen)
    if System == "BinarySystem": # with a planet ofc
        BinaryStarSystem(Keys[pygame.K_SPACE], screen)
    if System =="ElipticalSystem":
        elipticalOrbitSystem(Keys[pygame.K_SPACE], screen)
    if System == "L4 and L5":
        LagrangianPointDemoSystem(Keys[pygame.K_SPACE], screen)
    if System == "ThreeBody":
        ThreeBodyChaos(Keys[pygame.K_SPACE], screen)
    if System == "HorseShoe":
        HorseShoeCrabSystem(Keys[pygame.K_SPACE], screen)
    if System == "SlingShot":
        SlingShot(Keys[pygame.K_SPACE], screen)

def mainSIM(System, screen=None):
    global plotBodies
    plotBodies = []
    global SCALE1 # I have no idea why i have to do this but if i dont do this, it falls apart lmao (4/5/2026: now that i think about it, it makes sense lmao)
    global CenterPosx
    global CenterPosy
    global SYSTEM
    global TOTAL_PE
    global TOTAL_KE
    global TOTAL_E
    global comX
    global comY
    pygame.init()
    SCALE1 = 250/AU
    CenterPosx = (WIDTH/2)
    CenterPosy = (HEIGHT/2)
    pygame.display.set_caption("Planetary Bodies Simulation")
    if screen is None:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
    running = True
    bodies.clear()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        E = 0
        KE = 0
        PE = 0
        E, KE, PE = calcEnergy()
        screen.fill(BLACK)
        Keys= pygame.key.get_pressed()
        # TimestepControls() #()
        CamControls()
        
        comX, comY = calcCenterOfMass() #Center of Mass 
        
        Sim(System, screen)
        if SHOW_ENERGY:
            TOTAL_E.append(E)
            TOTAL_KE.append(KE)
            TOTAL_PE.append(PE)
        pygame.display.flip()
    # Keep pygame initialized so the main menu can continue using the same display
    if SHOW_ENERGY:
        graphEnergies(TOTAL_E, TOTAL_KE, TOTAL_PE)
    if PLTORNOT == True and TYPEPLT ==  "Velocity" or TYPEPLT == "all":
        graphVelocity(plotBodies)
    if PLTORNOT == True and TYPEPLT == "COM" or TYPEPLT == "all":
        graphCOM(plotBodies)
    if PLTORNOT == True and TYPEPLT == "Position" or TYPEPLT == "all":
        graphPosition(plotBodies)
    if PLTORNOT == True and TYPEPLT == "Position3D" or TYPEPLT == "all":
        graphPosition3D(plotBodies)

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
Saturn = Body("Saturn", 5.683e26, 60268e3, (227, 224, 192), 9.56 * AU, 0)
Saturn.velY = -9680
Uranus = Body("Uranus", 8.681e25, 25362e3, (172, 229, 238), 19.2 * AU, 0) #LMAO
Uranus.velY = -6810
Neptune = Body("Neptune", 1.024e26, 24764e3, (124, 183, 187), 30.1 * AU, 0)
Neptune.velY = -5430

#Not so real data, but still fun to watch :D
StarA = Body("StarA", 2e30, 700000e3, YELLOW, AU * 2.3, -0.4 * AU)
StarB = Body("StarB", 2e30, 700000e3, WHITE, AU * 2.3, 0.4 * AU)
X1Planet = Body("X1Planet", 5e26, 70005e3, CYAN, AU * 2, AU)
StarA.velX = -10000 
StarB.velX = -40000
X1Planet.velY = -20000

Star1 = Body("Star1", 10e30, 10000e5, RED, -AU, 0)
bodyC = Body("BodyC", 1e25, 5000e2, GREY, AU*0.6, 0)
bodyC.velY = -18000

BigPlanetForSlingShot = Body("big ahh planet", 2e31, 69911e4, CYAN, 0, 0)
BigPlanetForSlingShot.velX = 24000
ProbeA = Body("Probe", 1e25, 500e3, GREY, AU*0.6, -AU*0.6)
ProbeA.velY = 54000
ProbeA.velX = -54000

x = 15000

tbody1 = Body("Star1", 2e30, 5e8, YELLOW, -AU, -AU)
tbody1.velX = -x
tbody1.velY = x *3
tbody2 = Body("Star2", 1e31, 5e8, YELLOW, 0, 0)
tbody2.velX = 2 * -x
tbody2.velY = 2 * x
tbody3 = Body("Star3", 1e30, 5e8, YELLOW, AU, -AU)
tbody3.velX = -x *2
tbody3.velY = x

obj = Body("Horse Shoe Crab Orbit Satellite", 7e22, 1737.4e3, WHITE, 1.05 * AU, 0 )
obj.velY = -25000

b = [Sun, Earth, Moon, Mars, Mercury, Venus, Jupiter, Saturn, Neptune]

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

sling=[ProbeA, BigPlanetForSlingShot]
crab=[Sun, Earth, obj]
chaos=[tbody1, tbody2, tbody3]
pointdemo=[Sun, Earth, LagrangePoint4Asteroid, LagrangePoint5Asteroid]
eliptical=[Star1, bodyC]
binary=[StarA, StarB, X1Planet]

class MenuButton():
    def __init__(self, x, y, width, height, text, system, color=(40, 40, 40)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.system = system
        self.font = pygame.font.Font(None, 36)
        self.color = color
    
    def draw(self, screen):
        glowRect = pygame.Rect(self.rect.x - 5, self.rect.y - 5, self.rect.width + 10, self.rect.height + 10)
        pygame.draw.rect(screen, (100, 100, 100), glowRect, border_radius=5)
        
        mouse = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse)
        
        color = (100, 100, 100) if hovered else self.color
        
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=5)
        
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        
        screen.blit(text_surface, text_rect)
    
    def clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

simulations = [
    {"title": "Solar System",
    "system": "SolarSystem",
    "description": "Simulate the motion of planets in our Solar System."},
    {"title": "Binary Star System",
    "system": "BinarySystem",
    "description": "Simulate the motion of two stars orbiting each other."},
    {"title": "Eliptical Orbit System",
    "system": "ElipticalSystem",
    "description": "Simulate the motion of a body in an elliptical orbit."},
    {"title": "Lagrange Points Demonstration",
    "system": "L4 and L5",
    "description": "Simulate the motion of asteroids at the Lagrange points."},
    {"title": "Three Body Chaos",
    "system": "ThreeBody",
    "description": "Simulate the motion of three bodies interacting through gravity."},
    {"title": "Horse Shoe Crab Orbit",
    "system": "HorseShoe",
    "description": "Simulate the motion of a body in a horseshoe orbit."},
    {"title": "Gravitational Sling Shot",
    "system": "SlingShot",
    "description": "Simulate the motion of a body being slung around a planet."}
]

def mainMenuUwU():
    global SHOW_TRAIL
    global LINE2COM
    global TIMESTEP
    global TRAIL_LENGTH
    global PLTORNOT, TYPEPLT
    global SHOW_ENERGY
    global PLTVELOCITY
    
    pygame.init()
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space In YOUR Place Menu")
    clock = pygame.time.Clock()
    running = True
    
    selectedSim = None
    
    toggleTrailButton = MenuButton(560, 180, 400, 50, "Toggle Trail", "toggleTrail")
    
    toggleCOMButton = MenuButton(560, 240, 400, 50, "Toggle Center of Mass Line", "toggleCOM")
    
    cliButton = MenuButton(560, 300, 400, 50, "Initiate CLI", "initiateCLI")
    
    
    timestepSlider = Slider(screen, 560, 480, min=6, max=7200, initial=TIMESTEP, label="Time Step (seconds)", width=200, height=15)
    trailLengthSlider = Slider(screen, 560, 520, min=0, max=1000, initial=TRAIL_LENGTH, label="Trail Length (points)", width=200, height=15)
    
    stars = []
    
    for i in range(250):
        
        stars.append([random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3)])
    
    y = 140
    buttons = []
    utilityButtons = [toggleTrailButton, toggleCOMButton, cliButton]
    for sim in simulations:
        button = MenuButton(100, y, 400, 50, sim["title"], sim["system"])
        buttons.append(button)
        y += 60
    
    
    while running:
        clock.tick(60)
        
        screen.fill(BLACK)
        
        panel = pygame.Surface((480, HEIGHT - 200))
        panel.set_alpha(180)
        panel.fill((30, 30, 45))
        screen.blit(panel, (540, 120))
        
        settingsFont = pygame.font.Font(None, 32)
        settingsText = settingsFont.render("Settings", True, WHITE)
        screen.blit(settingsText, (700, 130))
        
        infoFont = pygame.font.Font(None, 22)
        
        timestepText = infoFont.render(f"Time Step: {TIMESTEP:.2f} seconds", True, WHITE)
        screen.blit(timestepText, (560, 360))
        
        trailLengthText = infoFont.render(f"Trail Length: {TRAIL_LENGTH} points", True, WHITE)
        screen.blit(trailLengthText, (560, 390))
        
        trailStatusText = infoFont.render(f"Show Trail: {'On' if SHOW_TRAIL else 'Off'}", True, WHITE)
        screen.blit(trailStatusText, (560, 420))
        
        comLineStatusText = infoFont.render(f"Show COM Line: {'On' if LINE2COM else 'Off'}", True, WHITE)
        screen.blit(comLineStatusText, (560, 450))
        
        title_font = pygame.font.Font(None, 48)
        title = title_font.render("Space In YOUR Place", True, WHITE)
        
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
        
        for star in stars:
            pygame.draw.circle(screen, WHITE, (star[0], star[1]), star[2])
            star[1] = star[1] + 0.5
            star[0] = star[0] + 0.5
            
            if star[1] > HEIGHT:
                star[1] = 0
            if star[0] > WIDTH:
                star[0] = 0
        
        for button in buttons:
            button.draw(screen)
        
        for button in utilityButtons:
            button.draw(screen)
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            
            for button in utilityButtons:
                if button.clicked(event):
                    if button.system == "toggleTrail":
                        SHOW_TRAIL = not SHOW_TRAIL
                    elif button.system == "toggleCOM":
                        LINE2COM = not LINE2COM
                    elif button.system == "initiateCLI":
                        MAIN()
            for button in buttons:
                if button.clicked(event):
                    PLTORNOT, TYPEPLT = askPlotterGUI()
                    SHOW_ENERGY = False
                    PLTVELOCITY = False
                    if PLTORNOT:
                        if TYPEPLT == "Velocity" or TYPEPLT == "all":
                            PLTVELOCITY = True
                        if TYPEPLT == "Energy" or TYPEPLT == "all":
                            SHOW_ENERGY = True
                    mainSIM(button.system, screen)
                    if not pygame.display.get_init() or pygame.display.get_surface() is None:
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
                        pygame.display.set_caption("Space In YOUR Place Menu")
        TIMESTEP = timestepSlider.getValue()
        TRAIL_LENGTH = trailLengthSlider.getValue()

        pygame_widgets.update(events)
        pygame.display.flip()


def MAIN():
    running = True
    global TIMESTEP
    global TRAIL_LENGTH
    global SHOW_ENERGY
    global PLTORNOT
    global TYPEPLT
    global SHOW_TRAIL
    global PLTVELOCITY
    global LINE2COM
    global WIDTH
    global HEIGHT
    printASCII()
    print("==============================-Evyvaan Singh - 2026-==============================")
    print("\nWelcome To 'Planetary Body Simulation'! ")
    print("\n \n \nPlease Choose the desired system (By entering the corresponding number) to start the simulation or enter commands. \n You can move around space in the simulation by using the keys 't', 'f', 'g' and 'h'. You can also zoom in and out by using the keys 'w' and 's' respectively. \n \n -Our Solar System (1) \n -Binary Star System (2) \n -System in which the the satellite planet follows an Eliptical Path (3) \n -Demonstration of simulation of bodies in L4 AND L5 points (4) \n -Three body chaotic system (5) \n -A system in which a satellite follows a 'Horseshoe' shaped orbit (6) \n -A probe experiencing a gravitational sling shot (7)")
    while running:
        choose = input(">>> ")
        if choose == "1":
            PLTORNOT, TYPEPLT = askPlotter()
            print("Task Started Successfully! \nYou can leave the program by entering 'exit'.")
            print("\nNow simulating, the Solar System.")
            if PLTORNOT:
                if TYPEPLT == "Velocity" or TYPEPLT == "all":
                    PLTVELOCITY = True
                if TYPEPLT == "Energy" or TYPEPLT == "all":
                    SHOW_ENERGY = True
                print("Trying to plot the data, this may take a while...")
            mainSIM("SolarSystem")
            print("It is recommended to restart the entire program to run another simulation. (You can restart by typing 'restart') \n====Simulation Ended====")
        elif choose == "2":
            PLTORNOT, TYPEPLT = askPlotter()
            print("Task Started Successfully! \nYou can leave the program by entering 'exit'.")
            print("Task Started Successfully! \n You can leave the program by entering 'exit'.")
            print("Now simulating, the Binary Stars System.")
            if PLTORNOT:
                if TYPEPLT == "Velocity" or TYPEPLT == "all":
                    PLTVELOCITY = True
                if TYPEPLT == "Energy" or TYPEPLT == "all":
                    SHOW_ENERGY = True
                print("Trying to plot the data, this may take a while...")
            mainSIM("BinarySystem")
            print("It is recommended to restart the entire program to run another simulation. (You can restart by typing 'restart') \n====Simulation Ended====")
        elif choose == "3":
            PLTORNOT, TYPEPLT = askPlotter()
            print("Task Started Successfully! \nYou can leave the program by entering 'exit'.")
            print("Task Started Successfully! \n You can leave the program by entering 'exit'.")
            print("Now simulating, a system in which the planet follows an elliptical orbit.")
            if PLTORNOT:
                if TYPEPLT == "Velocity" or TYPEPLT == "all":
                    PLTVELOCITY = True
                if TYPEPLT == "Energy" or TYPEPLT == "all":
                    SHOW_ENERGY = True
                print("Trying to plot the data, this may take a while...")
            mainSIM("ElipticalSystem")
            print("It is recommended to restart the entire program to run another simulation. (You can restart by typing 'restart') \n====Simulation Ended====")
        elif choose == "4":
            PLTORNOT, TYPEPLT = askPlotter()
            print("Task Started Successfully! \nYou can leave the program by entering 'exit'.")
            print("Task Started Successfully! \n You can leave the program by entering 'exit'.")
            print("Now simulating, the Earth and the Sun with two asteroid on L4 and L5 (With Diagram Lines)")
            if PLTORNOT:
                if TYPEPLT == "Velocity" or TYPEPLT == "all":
                    PLTVELOCITY = True
                if TYPEPLT == "Energy" or TYPEPLT == "all":
                    SHOW_ENERGY = True
                print("Trying to plot the data, this may take a while...")
            mainSIM("L4 and L5")
            print("It is recommended to restart the entire program to run another simulation. (You can restart by typing 'restart') \n ====Simulation Ended====")
        elif choose == "5":
            PLTORNOT, TYPEPLT = askPlotter()
            print("Task Started Successfully! \nYou can leave the program by entering 'exit'.")
            print("Task Started Successfully! \n You can leave the program by entering 'exit'.")
            print("Now simulating, a three body chaptic system. Best with low timestep.")
            if PLTORNOT:
                if TYPEPLT == "Velocity" or TYPEPLT == "all":
                    PLTVELOCITY = True
                if TYPEPLT == "Energy" or TYPEPLT == "all":
                    SHOW_ENERGY = True
                print("Trying to plot the data, this may take a while...")
            mainSIM("ThreeBody")
            print("It is recommended to restart the entire program to run another simulation. (You can restart by typing 'restart') \n ====Simulation Ended====")
        elif choose == "6":
            PLTORNOT, TYPEPLT = askPlotter()
            print("Task Started Successfully! \nYou can leave the program by entering 'exit'.")
            print("Task Started Successfully! \n You can leave the program by entering 'exit'.")
            print("Now simulating, a three body chaptic system. Best with low timestep.")
            if PLTORNOT:
                if TYPEPLT == "Velocity" or TYPEPLT == "all":
                    PLTVELOCITY = True
                if TYPEPLT == "Energy" or TYPEPLT == "all":
                    SHOW_ENERGY = True
                print("Trying to plot the data, this may take a while...")
            mainSIM("HorseShoe")
            print("It is recommended to restart the entire program to run another simulation. (You can restart by typing 'restart') \n ====Simulation Ended====")
        elif choose == "7":
            PLTORNOT, TYPEPLT = askPlotter()
            print("Task Started Successfully! \nYou can leave the program by entering 'exit'.")
            print("Task Started Successfully! \n You can leave the program by entering 'exit'.")
            print("Now simulating, a Sling Shot (With a probe)")
            if PLTORNOT:
                if TYPEPLT == "Velocity" or TYPEPLT == "all":
                    PLTVELOCITY = True
                if TYPEPLT == "Energy" or TYPEPLT == "all":
                    SHOW_ENERGY = True
                print("Trying to plot the data, this may take a while...")
            mainSIM("SlingShot")
            print("It is recommended to restart the entire program to run another simulation. (You can restart by typing 'restart') \n ====Simulation Ended====")
        elif choose == "exit" or choose == "quit":
            running = False
            print("'Bye'  -  Evyvaan said calmly")
            print("================================================================================================================================")
        elif choose.lower() == "skibidi" or choose.lower() == "skibidi toilet" or choose.lower() == "gyatt":
            running = False
            print("no. this is not allowed here")
        elif choose.lower() == "set-timestep":
            TIMESTEP = 60 * float(input("(Default is 60 x 60) Time Step: 60 x "))
            print(f"The timestep is {TIMESTEP}. Note that the default timestep is the most stable timestep.\n Increasing the timestep may lead to instability and innaccuracies in the simulation.")
        elif choose.lower() == "set-trail-lenght":
            TRAIL_LENGTH = int(input("Trail Lenght (Default is 500) = "))
            print(f"The Trail Lenght is {TRAIL_LENGTH}. Note that the bigger trails may cause performance issues")
        elif choose.lower() == "show":
            print(f"========-Variables and Constants in the simulation-======== \n 1 Astronomical Unit (Distance from the Sun to Earth): {AU} \n Gravitational Constant: {G} \n Default Scale: {SCALE1} \n Current Timestep: {TIMESTEP} \n Current Trail Lenght: {TRAIL_LENGTH} \n Show Trails: {SHOW_TRAIL} \n Show properties of all the planets in the solar system? (y/n)")
            if input("  >  ").lower() == "y" :
                for body in b:
                    print(f"====-{body.name}-==== \n Mass: {body.mass} kg \n Radius: {body.radius/1000} km \n Velocity: {math.hypot(body.velX, body.velY)/1000} km/s")
        elif choose.lower() == "set-trail":
            print("Toggling trail")
            if SHOW_TRAIL == True:
                SHOW_TRAIL = False
            else:
                SHOW_TRAIL = True
            print(f"Trail is now set to {SHOW_TRAIL}")
        elif choose.lower() == "set-com-line":
            print("Toggling line to center of mass")
            if LINE2COM == True:
                LINE2COM = False
            else:
                LINE2COM = True
            print(f"Line to center of mass is now set to '{LINE2COM}'")
        elif choose.lower() == "set-screen-size":
            WIDTH = int(input("Width (Default is 1200) = "))
            HEIGHT = int(input("Height (Default is 800) = "))
            print(f"Screen size is now set to {WIDTH} x {HEIGHT}. Note that smaller screen sizes may cause performance issues")
        elif choose.lower() == "help":
            print("HELP COMMAND \n General Commands: \n 'exit' or 'quit' - Exit the program \n 'restart' - Restart the program \n 'help' - Show this message \n 'show' - Show some of the variables and constants in the simulation \n 'set-timestep' - Set the timestep of the simulation (Default is 60 x 60 seconds)\n 'set-trail-lenght' - Set the lenght of the trails (Default is 500) \n 'set-trail' - Toggle trails on and off \n 'set-com-line' - Toggle line to center of mass on and off \n 'set-screen-size' - Set the screen size \n PLOTS \n Energy Plot: Plots the Kinetic, Potentioal and Total energy of the system with time \n Velocity Plot: Plots the velocity of the planets with time \n Center of Mass Plot: Plots the distance of the planets to the center of mass with time \n Position Plot: Plots the X and Y position of the planets with time \n Position 3D Plot: Plots the X and Y position of the planets in a 3D graph \n SIM CONTROLS \n You can pause and unpause the simulation by pressing the space bar while the simulation is running. \n You can move around space in the simulation by using the keys 't', 'f', 'g' and 'h'. You can also zoom in and out by using the keys 'w' and 's' respectively. \n PHYSICAL INFO \n The units are: Meters, Kilograms, Seconds. The default timestep is 60 x 60 seconds, which means that every second in the simulation is equal to 1 hour in real life. The default scale is 250 pixels per Astronomical Unit (AU), which means that the distance from the Sun to the Earth will be represented as 250 pixels on the screen.")
        elif choose.lower() == "restart":
            print("Restarting... ")
            script_path = os.path.abspath(__file__)
            
            python = sys.executable
            subprocess.Popen([python, script_path])
            sys.exit()
            print("'Bye'  -  Evyvaan said calmly")
            print("================================================================================================================================")
        else:
            print("Invalid Command")
    sys.exit()

# MAIN()
mainMenuUwU()
