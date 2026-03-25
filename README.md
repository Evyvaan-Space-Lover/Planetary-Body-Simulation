# Planetary Body Simulation

A real-time N-body gravitational simulation built using Python and Pygame.
This project models planetary motion, multi-body systems, and orbital mechanics using Verlet integration for improved stability and energy behavior.

---

##  Features

-  Realistic planetary motion (approximate physical scaling)
-  Binary star system with orbiting planet
-  Three-body chaotic system
-  Gravitational slingshot simulation
-  Lagrange points (L4 & L5)
-  Horseshoe orbit system
-  Energy and velocity plotting (matplotlib)
-  Smooth orbital trails
-  Camera movement and zoom

---

##  Physics & Concepts

- Newtonian Gravity
- N-body Simulation
- Verlet Integration
- Orbital Mechanics
- Energy Conservation (KE, PE, Total Energy)
- Chaotic Systems & Sensitivity to Initial Conditions

---

##  Controls (Simulation Window)

### Key| Action

SPACE| Pause / Resume simulation

W / S| Zoom in / out

T / G| Move camera up / down

F / H| Move camera left / right

R| Reset zoom

---

##  Console Commands (">>>")

### Run Systems

1 → Solar System 
2 → Binary Star System 
3 → Elliptical Orbit 
4 → L4 & L5 System 
5 → Three Body Chaos 
6 → Horseshoe Orbit 
7 → Slingshot Simulation 

###  General Commands

exit / quit → Close program 


restart → Restart simulation 


show → Display system parameters 

###  Settings

set-timestep → Change simulation timestep 


set-trail_length → Adjust trail length 


set-trail → Toggle trails on/off 



---

##  Data Visualization

After running simulations, you can generate plots using matplotlib:

- Velocity vs Time
- Energy vs Time (KE, PE, Total)

---

##  Installation & Run

Requirements

- Python 3.x
- pygame
- matplotlib

Install dependencies

pip install pygame matplotlib

Run the simulation

python SolarSystemSim.py

---

##  Notes

- Units are SI (meters, kilograms, seconds)
- Timestep significantly affects accuracy
- Large timesteps can introduce numerical errors
- Close encounters may produce sharp energy spikes
- Some systems (like 3-body) are inherently chaotic

---

##  Screenshots


---

##  Author

Evyvaan Singh
Project started: March 2025

---

##  License

This project is open for learning, experimentation, and modification.

---

##  Future Improvements

- Adaptive timestep
- Improved collision handling
- Higher-order numerical integrators
- UI and usability enhancements

---
