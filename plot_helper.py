import sys
import pickle
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

def plot_com(bodies):
    plt.figure()
    for b in bodies:
        plt.plot(b.get('DISTANCECOM', []), label=b.get('name',''))
    plt.legend()
    plt.title('Distance to Center of Mass vs Time')
    plt.xlabel('Frames')
    plt.ylabel('Distance to COM (in meters)')
    plt.show()

def plot_velocity(bodies):
    plt.figure()
    for b in bodies:
        plt.plot(b.get('VELOCITY', []), label=b.get('name',''))
    plt.legend()
    plt.title('Velocity vs Time')
    plt.xlabel('Frames')
    plt.ylabel('Velocity (in m/s)')
    plt.show()

def plot_position(bodies):
    plt.figure()
    for b in bodies:
        x = b.get('X', [])
        y = [-val for val in b.get('Y', [])]
        plt.plot(x, y, label=b.get('name',''))
    plt.legend()
    plt.title('Trajectory (X vs Y)')
    plt.xlabel('X Trajectory (in meters)')
    plt.ylabel('Y Trajectory (in meters)')
    plt.show()

def plot_position3d(bodies):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for b in bodies:
        x = b.get('X', [])
        y = [-val for val in b.get('Y', [])]
        time = range(len(x))
        ax.plot(x, y, time, label=b.get('name',''))
    ax.set_title('3D Trajectory (X vs Y vs Time)')
    ax.set_xlabel('X Position (in meters)')
    ax.set_ylabel('Y Position (in meters)')
    ax.set_zlabel('Time (in seconds)')
    ax.legend()
    ax.view_init(elev=30, azim=120)
    plt.show()

def plot_energy(payload):
    plt.figure()
    plt.plot(payload.get('TOTAL_E', []), label='Total Energy Of the System')
    plt.plot(payload.get('TOTAL_KE', []), label='Total Kinetic Energy of the System')
    plt.plot(payload.get('TOTAL_PE', []), label='Total Potential Energy of the System')
    plt.legend()
    plt.title('Energy vs Time')
    plt.xlabel('Frames')
    plt.ylabel('Energy (In Joules)')
    plt.show()


def main():
    if len(sys.argv) < 2:
        print('Usage: plot_helper.py <data.pkl>')
        return
    path = sys.argv[1]
    if not os.path.exists(path):
        print('Data file not found:', path)
        return
    try:
        with open(path, 'rb') as f:
            data = pickle.load(f)
    except Exception as e:
        print('Failed to load data:', e)
        return

    t = data.get('type')
    if t == 'COM':
        plot_com(data.get('bodies', []))
    elif t == 'Velocity':
        plot_velocity(data.get('bodies', []))
    elif t == 'Position':
        plot_position(data.get('bodies', []))
    elif t == 'Position3D':
        plot_position3d(data.get('bodies', []))
    elif t == 'Energy':
        plot_energy(data)

if __name__ == '__main__':
    main()
