"""
This script has been developed to allow the comparison of different discs using examples from the shotshaper package.
It combines the original disc_gui2d.py and disc_golf_throw.py script from the examples folder.
It has been modified to allow multiple disc throws to be overlaid and compare the results. 
Additional it can use either metric or imperial units for the plots and sliders.

This script developed by Chris Egan in support of Trash Panda Disc Golf
chris.egan@ceganconsulting.com


Open Items to correct:
 - the coefficient plots need dynamic scaling for some plots
 - unit conversion is not working yet everywhere. 
"""

from shotshaper.projectile import DiscGolfDisc
import matplotlib.pyplot as pl
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider, Button, TextBox
import numpy as np
from shotshaper.transforms import T_21
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import sys
import argparse

#create Parser
parser = argparse.ArgumentParser(description="Launch Shotshaper with specified disc data files and units.")

# Add an argument for unit selection with default value 'imperial'
parser.add_argument('--units', type=str, default='metric', choices=['metric', 'imperial'],
                    help='Unit system to use (metric or imperial). Default is metric. All calculations are done in metric and converted if desired.')

# Add an argument for disc data files (positional arguments)
parser.add_argument('discs', nargs='+', help='Names of the disc data files.')

# Parse the arguments
args = parser.parse_args()

# Extract the unit system and disc names from args
unit_system = args.units
disc_names = []
disc_names = args.discs

# Limit the number of discs to 6
# This limit can be increased, but the plots will become overly crowded
num_discs = len(disc_names)
if len(disc_names) > 6:
    print("Over max allowable, terminating")
    sys.exit(1)


def disc_vertices(attitude):
    a,nt = attitude.shape
    nvert = 40
    r = np.linspace(0, 2*np.pi, nvert)
    xd = np.cos(r)
    yd = np.sin(r)
    zd = np.zeros(nvert)
    discoutline = np.vstack((xd, yd, zd)).T
    p=0
    while p < nvert:
        discoutline[p] = np.matmul(T_21(attitude[:,0]), discoutline[p]) # Convert outline from disc coords to ground coords
        p += 1
    d = [list(zip(discoutline[:,0],discoutline[:,1],discoutline[:,2]))]
    
    return d


#print(num_discs)

#starting parameters
mass = 0.175
speed = 24
z0 = 1.3
pos = np.array((0,0,z0))
pitch = 5.00
nose = 0.0
roll = 1.0  
yaw = 0
adjust_axes = False

#conversion factors for imperial units
m2ft_factor = 3.28084 if unit_system == 'imperial' else 1
mph_factor = 2.23694 if unit_system == 'imperial' else 1
N2ozf_factor = 3.59694 if unit_system == 'imperial' else 1
Nm2inlb_factor = 8.85075 if unit_system == 'imperial' else 1
rad2deg_factor = 57.2958 if unit_system == 'imperial' else 1

#Array to hold disc objects
discs = []
for disc in disc_names:
    discs.append(DiscGolfDisc(disc, mass=mass))
    
# Array to hold omega values
omegas = []
for disc in discs:
    omegas.append(disc.empirical_spin(speed))

# Array to hold shot data
shots = []
for i, (disc, omega) in enumerate(zip(discs, omegas)):
    shots.append(disc.shoot(speed=speed, omega=omega, pitch=pitch, position=pos, nose_angle=nose, roll_angle=roll,yaw=yaw))
    
# Array to hold position data
positions = []

for shot in shots:
    #extract postition data
    x, y, z = shot.position * m2ft_factor
    positions.append((x, y, z))
    

# Post Processed Data
post_arrays = []
velocity_arrays = []

for disc, shot, omega in zip(discs, shots, omegas):
    post = disc.post_process(shot, omega)
    post_array = np.array(post)
    post_arrays.append(post_array)
    velocity_arrays.append(shot.velocity)

# Function to close all figures if one is closed
def close_all_figures(event):
    pl.close('all')


# Creating figures
fig1 = pl.figure(figsize=(13, 6), dpi=100)
#fig1.canvas.set_window_title('Drift vs Height')
fig1.suptitle('Drift vs Height Plot')
fig1.canvas.mpl_connect('close_event', close_all_figures)

fig2 = pl.figure(figsize=(13, 4), dpi=100)
#fig2.canvas.set_window_title('Distance vs Height')
fig2.suptitle('Distance vs Height Plot')
fig2.canvas.mpl_connect('close_event', close_all_figures)

fig3 = pl.figure(figsize=(13, 6), dpi=110)
#fig3.canvas.set_window_title('Distance vs Drift')
fig3.suptitle('Distance vs Drift Plot')
fig3.canvas.mpl_connect('close_event', close_all_figures)

fig_sliders = pl.figure(figsize=(8, 4), dpi=100)
#fig_sliders.canvas.set_window_title('Adjustment Sliders')
fig_sliders.suptitle('Adjust Throw Parameters')
fig_sliders.canvas.mpl_connect('close_event', close_all_figures)

ax1 = fig3.add_subplot(1,1,1)
ax2 = fig2.add_subplot(1,1,1)
ax3 = fig1.add_subplot(1,1,1)


# Set fixed plot limits
ax1.axis((0, 500, -100, 100))  # Distance vs Drift
ax2.axis((0, 500, 0, 50))  # Distance vs Height
ax3.axis((-50, 50, 0, 50))  # Drift vs Height
        
ax3.invert_xaxis()

if unit_system == 'imperial':
    ax1.set_xlabel('Distance (ft)')
    ax1.set_ylabel('Drift (ft)')

    ax2.set_xlabel('Distance (ft)')
    ax2.set_ylabel('Height (ft)')

    ax3.set_xlabel('Drift (ft)')
    ax3.set_ylabel('Height (ft)')
if unit_system == 'metric':
    ax1.set_xlabel('Distance (m)')
    ax1.set_ylabel('Drift (m)')

    ax2.set_xlabel('Distance (m)')
    ax2.set_ylabel('Height (m)')

    ax3.set_xlabel('Drift (m)')
    ax3.set_ylabel('Height (m)')

# For the Distance vs Drift plot
ax1.set_aspect(1)  

# For the Distance vs Height plot
ax2.set_aspect(2)  

# For the Drift vs Height plot
ax3.set_aspect(1) 

# Array to hold line objects
lines = []

for i, ((x, y, z), disc_name) in enumerate(zip(positions, disc_names)):
    # Plotting on ax1: x vs. y
    line, = ax1.plot(x, y, lw=2, label=disc_name)
    lines.append(line)  # Store the line object if needed for later
    
    # Plotting on ax2: x vs. z
    line, = ax2.plot(x, z, lw=2, label=disc_name)
    lines.append(line)  # Store the line object if needed for later
    
    # Plotting on ax3: y vs. z
    line, = ax3.plot(y, z, lw=2, label=disc_name)
    lines.append(line)  # Store the line object if needed for later

ax1.legend()
ax2.legend()
ax3.legend()

# Alignment parameters for sliders
left_alignment = 0.25  # Adjust this value to center the sliders
slider_width = 0.5  # Adjust this to control the width of the sliders
slider_height = 0.04  # Adjust this to control the height of the sliders
slider_sepation = 0.1  # Adjust this to control the separation between sliders
first_bottom = 0.80  # Adjust this to control the vertical position of the first slider

# Adjust the slider axes to be associated with the new figure
ax4  = fig_sliders.add_axes([left_alignment, first_bottom, slider_width, slider_height], facecolor='lightgrey')
ax5  = fig_sliders.add_axes([left_alignment, first_bottom - (slider_sepation * 1), slider_width, slider_height], facecolor='lightgrey')
ax6  = fig_sliders.add_axes([left_alignment, first_bottom - (slider_sepation * 2), slider_width, slider_height], facecolor='lightgrey')
# ax7  = fig_sliders.add_axes([left_alignment, 0.65, slider_width, slider_height], facecolor='lightgrey') # Uncomment or adjust as needed
ax8  = fig_sliders.add_axes([left_alignment, first_bottom - (slider_sepation * 3), slider_width, slider_height], facecolor='lightgrey')
ax9  = fig_sliders.add_axes([left_alignment, first_bottom - (slider_sepation * 4), slider_width, slider_height], facecolor='lightgrey')
ax11 = fig_sliders.add_axes([left_alignment, first_bottom - (slider_sepation * 5), slider_width, slider_height], facecolor='lightgrey')


if unit_system == 'imperial':
    s1 = Slider(ax=ax4, label='Speed (mph)', valmin=30,  valmax=80, valinit=speed * mph_factor)
else:
    s1 = Slider(ax=ax4, label='Speed (m/s)', valmin=13.4,  valmax=35.8, valinit=speed)
s2 = Slider(ax=ax5, label='Roll (deg)',   valmin=-110, valmax=110, valinit=roll)
s3 = Slider(ax=ax6, label='Pitch (deg)', valmin=-10,   valmax=50, valinit=pitch)
s5 = Slider(ax=ax8, label='Nose (deg)',   valmin=-10, valmax=10, valinit=nose)
s7 = Slider(ax=ax9, label='Mass (g)',   valmin=140, valmax=200, valinit=mass*1000)
s6 = Slider(ax=ax11, label='Spin (-)',   valmin=0, valmax=2, valinit=1.0)

#post process figure
fig4, axes = pl.subplots(nrows=2, ncols=3, dpi=80, figsize=(13, 5))
fig4.canvas.mpl_connect('close_event', close_all_figures)

lines_lifts = []
lines_drags = []
lines_moms = []
lines_alphas = []
lines_velocities_u = []
# lines_velocities_v = []  # Uncomment if using
# lines_velocities_w = []  # Uncomment if using
lines_rolls = []
lines_arc = []


for i, (post_array, velocities) in enumerate(zip(post_arrays, velocity_arrays)):
    arc = post_array[0] * m2ft_factor
    lifts = post_array[3] * N2ozf_factor
    drags = post_array[4] * N2ozf_factor
    moms = post_array[5] * Nm2inlb_factor
    alphas = post_array[1]
    rolls = post_array[6] * rad2deg_factor
    betas = post_array[2]
    
    velocities_u = velocities[0, :]  # Assuming the first row is 'u' velocities

  
    line, = axes[0, 0].plot(arc, lifts, label=disc_names[i])
    lines_lifts.append(line)

    line, = axes[0, 1].plot(arc, drags, label=disc_names[i])
    lines_drags.append(line)

    line, = axes[0, 2].plot(arc, moms, label=disc_names[i])
    lines_moms.append(line)

    line, = axes[1, 0].plot(arc, alphas, label=disc_names[i])
    lines_alphas.append(line)

    line, = axes[1, 1].plot(arc, velocities_u, label=disc_names[i])
    lines_velocities_u.append(line)

    line, = axes[1, 2].plot(arc, rolls, label=disc_names[i])
    lines_rolls.append(line)
   

# After creating all line objects, ensure legends are displayed
for ax in axes.flat:
    ax.legend()


# Set labels and legends
if unit_system == 'imperial':  # Fix units and conversions, not complete
    axes[0, 0].set_xlabel('Distance (ft)')
    axes[0, 0].set_ylabel('Lift force (ozf)')
    axes[0, 1].set_xlabel('Distance (ft)')
    axes[0, 1].set_ylabel('Drag force (ozf)')
    axes[0, 2].set_xlabel('Distance (ft)')
    axes[0, 2].set_ylabel('Moment (in-lb)')
    axes[1, 0].set_xlabel('Distance (ft)')
    axes[1, 0].set_ylabel('Angle of attack (deg)')
    axes[1, 1].set_xlabel('Distance (ft)')
    axes[1, 1].set_ylabel('Velocities (mph)')
    axes[1, 1].legend()
    axes[1, 2].set_xlabel('Distance (ft)')
    axes[1, 2].set_ylabel('Roll rate (deg/s)')
    
if unit_system == 'metric':
    axes[0, 0].set_xlabel('Distance (m)')
    axes[0, 0].set_ylabel('Lift force (N)')
    axes[0, 1].set_xlabel('Distance (m)')
    axes[0, 1].set_ylabel('Drag force (N)')
    axes[0, 2].set_xlabel('Distance (m)')
    axes[0, 2].set_ylabel('Moment (Nm)')
    axes[1, 0].set_xlabel('Distance (m)')
    axes[1, 0].set_ylabel('Angle of attack (deg)')
    axes[1, 1].set_xlabel('Distance (m)')
    axes[1, 1].set_ylabel('Velocities (m/s)')
    axes[1, 1].legend()
    axes[1, 2].set_xlabel('Distance (m)')
    axes[1, 2].set_ylabel('Roll rate (rad/s)')

pl.tight_layout()

def update(x):
    speed = s1.val / mph_factor
    roll = s2.val
    pitch = s3.val
    nose = s5.val
    spin = s6.val
    mass = s7.val / 1000
    
    global discs
    discs = [DiscGolfDisc(disc_name, mass=mass) for disc_name in disc_names]
    
    global omegas
    omegas = [disc.empirical_spin(speed) for disc in discs]
    
    global shots
    shots = [disc.shoot(speed=speed, omega=omega, pitch=pitch, position=pos, nose_angle=nose, roll_angle=roll,yaw=yaw) for disc, omega in zip(discs, omegas)]
    
    global positions
    positions = [(x * m2ft_factor, y * m2ft_factor, z * m2ft_factor) for shot in shots for x, y, z in [shot.position]]

    #Post Processed Data
    
    post_arrays = []
    velocity_arrays = []

    for disc, shot, omega in zip(discs, shots, omegas):
        post = disc.post_process(shot, omega)
        post_array = np.array(post)
        post_arrays.append(post_array)
        velocity_arrays.append(shot.velocity)
    
    global lines
    
    for i, (x, y, z) in enumerate(positions):
        # Assuming every 3 lines correspond to the same disc but different plots
        lines[3*i].set_xdata(x)
        lines[3*i].set_ydata(y)
        
        lines[3*i + 1].set_xdata(x)
        lines[3*i + 1].set_ydata(z)
        
        lines[3*i + 2].set_xdata(y)
        lines[3*i + 2].set_ydata(z)
        
  
    for i, (post_array, velocities) in enumerate(zip(post_arrays, velocity_arrays)):
        arc = post_array[0] * m2ft_factor
        lifts = post_array[3] * N2ozf_factor
        drags = post_array[4] * N2ozf_factor
        moms = post_array[5] * Nm2inlb_factor
        alphas = post_array[1]
        rolls = post_array[6] * rad2deg_factor
        betas = post_array[2]
        
        velocities_u = velocities[0, :]  # Assuming the first row is 'u' velocities
        
        
        lines_lifts[i].set_xdata(arc)
        lines_lifts[i].set_ydata(lifts)
        
        lines_drags[i].set_xdata(arc)
        lines_drags[i].set_ydata(drags)
        
        lines_moms[i].set_xdata(arc)
        lines_moms[i].set_ydata(moms)
        
        lines_alphas[i].set_xdata(arc)
        lines_alphas[i].set_ydata(alphas)
        
        lines_velocities_u[i].set_xdata(arc)
        lines_velocities_u[i].set_ydata(velocities_u)
        
        lines_rolls[i].set_xdata(arc)
        lines_rolls[i].set_ydata(rolls)

    
    # if adjust_axes:
    #     ax1.axis((min(x1),max(x1),min(y1),max(y1)))
    #     ax2.axis((min(x1),max(x1),min(z1),max(z1)))
    #     ax3.axis((min(y1),max(y1),min(z1),max(z1)))
        
    fig1.canvas.draw_idle()
    fig3.canvas.draw_idle()
    fig2.canvas.draw_idle()
    fig4.canvas.draw_idle()


s1.on_changed(update)
s2.on_changed(update)
s3.on_changed(update)
s5.on_changed(update)
s6.on_changed(update)
s7.on_changed(update)

pl.show()
    
