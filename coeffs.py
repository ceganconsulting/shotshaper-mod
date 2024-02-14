from shotshaper.projectile import DiscGolfDisc
import matplotlib.pyplot as pl
#from mpl_toolkits import mplot3d
#from mpl_toolkits.mplot3d import Axes3D
#from matplotlib.widgets import Slider, Button, TextBox
#import numpy as np
#from shotshaper.transforms import T_21
#from mpl_toolkits.mplot3d.art3d import Poly3DCollection
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

# Initialize subplots
fig, axs = pl.subplots(2, 2, figsize=(14, 10))
fig.subplots_adjust(hspace=0.3, wspace=0.3)

for name in disc_names:
    # Create an instance of DiscGolfDisc for each disc
    disc = DiscGolfDisc(name=name)
    
    # Angle of attack in degrees
    alpha = disc._alpha
    
    # Subplot 1: Cl vs. Alpha
    axs[0, 0].plot(alpha, disc._Cl, label=f'{name} $C_L$')
    axs[0, 0].set_title('$C_L$ vs. Angle of Attack')
    axs[0, 0].set_xlabel('Angle of Attack (degrees)')
    axs[0, 0].set_ylabel('$C_L$')
    axs[0, 0].legend()
    axs[0, 0].grid(True)
    
    # Subplot 2: Cd vs. Alpha
    axs[0, 1].plot(alpha, disc._Cd, label=f'{name} $C_D$')
    axs[0, 1].set_title('$C_D$ vs. Angle of Attack')
    axs[0, 1].set_xlabel('Angle of Attack (degrees)')
    axs[0, 1].set_ylabel('$C_D$')
    axs[0, 1].legend()
    axs[0, 1].grid(True)
    
    # Subplot 3: Cm vs. Alpha
    axs[1, 0].plot(alpha, disc._Cm, label=f'{name} $C_M$')
    axs[1, 0].set_title('$C_M$ vs. Angle of Attack')
    axs[1, 0].set_xlabel('Angle of Attack (degrees)')
    axs[1, 0].set_ylabel('$C_M$')
    axs[1, 0].legend()
    axs[1, 0].grid(True)
    
    # Subplot 4: Cl/Cd vs. Alpha
    Cl_Cd = disc._Cl / disc._Cd  # Aerodynamic efficiency
    axs[1, 1].plot(alpha, Cl_Cd, label=f'{name} $C_L/C_D$')
    axs[1, 1].set_title('$C_L/C_D$ vs. Angle of Attack')
    axs[1, 1].set_xlabel('Angle of Attack (degrees)')
    axs[1, 1].set_ylabel('$C_L/C_D$')
    axs[1, 1].legend()
    axs[1, 1].grid(True)

# Show the plot
pl.show()