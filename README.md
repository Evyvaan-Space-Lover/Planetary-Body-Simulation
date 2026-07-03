# Planetary Body Simulation

A real-time N-body gravitational simulator built using Python and Pygame. This project models orbital mechanics, chaotic systems, and various gravitational phenomena using Verlet Integration for improved numerical stability.

Originally created as a way to explore space physics and computational simulations, the project has evolved into an interactive educational tool capable of demonstrating a wide range of celestial dynamics.

---

## Features

### Orbital Systems

* Solar System Simulation
* Binary Star System
* Elliptical Orbit Demonstration
* Lagrange Point (L4 & L5) System
* Three-Body Chaotic System
* Horseshoe Orbit System
* Gravitational Slingshot Demonstration

### GUI Features

* Interactive simulation launcher
* Button-based system selection
* Slider-based parameter controls
* Plot-selection popup window
* Cleaner simulation workflow
* CLI fallback support

### Visualization Features

* Orbital trail rendering
* Camera movement controls
* Zoom controls
* Screenshot functionality
* Pause and resume functionality

### Data Analysis and Plotting

* Energy analysis (Kinetic Energy, Potential Energy, Total Energy)
* Velocity plotting
* 2D trajectory plotting
* 3D trajectory plotting using time as the third dimension

---

## Physics Concepts Demonstrated

* Newtonian Gravity
* N-body Interactions
* Orbital Mechanics
* Chaotic Dynamics
* Energy Conservation
* Numerical Integration
* Lagrange Points
* Gravitational Assists
* Horseshoe Orbits

---

## Numerical Method

The simulator uses Verlet Integration to update positions over time.

Compared to simpler methods such as Euler Integration, Verlet Integration offers improved long-term stability and better energy conservation for orbital simulations.

---

## Simulation Workflow

1. Launch the program.
2. Select the desired simulation using the GUI menu.
3. Adjust simulation settings using sliders/buttons.
4. Choose desired plots from the popup window.
5. Press START.
6. The simulation begins.

---

## Simulation Controls

| Key   | Action                    |
| ----- | ------------------------- |
| SPACE | Pause / Resume Simulation |
| W     | Zoom In                   |
| S     | Zoom Out                  |
| T     | Move Camera Up            |
| G     | Move Camera Down          |
| F     | Move Camera Left          |
| H     | Move Camera Right         |
| R     | Reset Camera and Zoom     |
| P     | Save Screenshot           |

---

## Console Commands

Although the simulator now includes a GUI launcher system, terminal commands are still supported.

### General Commands

```text
help

Display the help menu.

show

Display information about the current simulation.

restart

Restart the application.

exit
quit

Close the program.

---

System Selection

1

Solar System Simulation

2

Binary Star System

3

Elliptical Orbit Demonstration

4

Lagrange Point (L4 & L5) System

5

Three-Body Chaotic System

6

Horseshoe Orbit System

7

Gravitational Slingshot Demonstration

---

Simulation Settings

set-timestep

Change the simulation timestep.

Smaller timesteps generally improve numerical accuracy.

set-trail

Enable or disable orbital trails.

set-trail-length

Change the maximum trail length.

(These commands are still available through the CLI fallback system.)

---

Plots

Energy plot

Plot kinetic energy, potential energy, and total energy over time.

Velocity plot

Plot velocity over time.

Trajectory plot

Generate a two-dimensional trajectory plot.

Trajectory with time plot

Generate a three-dimensional trajectory plot using:

* X-axis → X Position
* Y-axis → Y Position
* Z-axis → Time
```
---

Screenshots

Screenshots of the simulation can be captured during runtime using the screenshot functionality.

Recommended showcase systems:

* Binary Star System
* Three-Body Chaos
* Horseshoe Orbit
* 3D Trajectory Visualization

---

Installation

Requirements

* Python 3.x
* pygame
* matplotlib
* numpy

Install dependencies:

pip install pygame matplotlib numpy

Run the simulation:

python SolarSystemSim.py

---

Executable Version

A standalone Windows executable is available under the GitHub Releases section (And separately in the repository too).

The executable includes all required dependencies and does not require Python to be installed.

---

Notes

* All quantities use SI units:
  
  * Distance → meters (m)
  * Mass → kilograms (kg)
  * Time → seconds (s)

* Large timesteps may introduce numerical inaccuracies.

* Chaotic systems are highly sensitive to initial conditions.

* This simulator is intended for educational and exploratory purposes.

---

Screenshots

"Binary Star System" (images/SimBinaryStarSys2.JPG) "Solar System" (images/SimSolarSys.JPG) "Solar System" (images/SimSolarSys2.JPG)  "Three Body System Velocity Plot" (images/ThreeBodyEnergyPlot(Timestep=60).png)  ---

---

Technical Challenges

During development, the project involved solving numerous challenges, including:

* Energy conservation issues
* Timestep selection and numerical stability
* Chaotic system behavior
* Restart functionality bugs
* Data collection for plotting
* Integrating 3D trajectory visualization
* GUI integration and workflow systems
* Packaging the simulator into a standalone executable

Many of these challenges required experimentation and iterative debugging, providing valuable experience in computational physics and software development.

---

Future Work

Potential future improvements include:

* True 3D simulations
* Adaptive timesteps
* Additional visualization tools
* More orbital systems
* Expanded GUI customization
* Real-time plotting tools
* Interactive body creation

---

Author

Evyvaan Singh

All simulation code was written by the author.

AI tools were used solely for assistance with documentation and README preparation.

---
