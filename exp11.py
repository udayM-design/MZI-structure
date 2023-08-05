import meep as mp
import numpy as np
import matplotlib.pyplot as plt

# Define the simulation cell size
cell_size = mp.Vector3(24, 16, 0)

# Define the PML boundary conditions
pml_layers = [mp.PML(1.0)]

# Define the resolution
resolution = 10

# Create the Meep simulation object
sim = mp.Simulation(cell_size=cell_size,
                    boundary_layers=pml_layers,
                    resolution=resolution)

# Define the waveguide parameters
waveguide_width = 1.0
waveguide_length = 10.0
waveguide_lengthh = 3.0
# Define the MZI parameters
splitter_length = 1.0
arm_length = 5.0
phase_shifter_length = 1.0

# Define the waveguide structures
waveguide1 = mp.Block(material=mp.Medium(index=1.5),
                      size=mp.Vector3(waveguide_lengthh, waveguide_width, mp.inf),
                      center=mp.Vector3(-waveguide_lengthh*2, 0, 0))

waveguide2 = mp.Block(material=mp.Medium(index=1.5),
                      size=mp.Vector3(waveguide_lengthh, waveguide_width, mp.inf),
                      center=mp.Vector3(waveguide_lengthh*2, 0, 0))

# Add the waveguide structures to the simulation cell
sim.geometry.append(waveguide1)
sim.geometry.append(waveguide2)

# Define the Y splitter structures
splitter1 = mp.Block(material=mp.Medium(index=1.5),
                     size=mp.Vector3(waveguide_width, splitter_length, mp.inf),
                     center=mp.Vector3(-waveguide_length/2, waveguide_width/2 + splitter_length/2, 0))

splitter2 = mp.Block(material=mp.Medium(index=1.5),
                     size=mp.Vector3(waveguide_width, splitter_length, mp.inf),
                     center=mp.Vector3(waveguide_length/2, waveguide_width/2 + splitter_length/2, 0))

# Add the Y splitter structures to the simulation cell
sim.geometry.append(splitter1)
sim.geometry.append(splitter2)

# Define the upper arm structures
upper_arm1 = mp.Block(material=mp.Medium(index=1.5),
                      size=mp.Vector3(arm_length, waveguide_width, mp.inf),
                      center=mp.Vector3(-waveguide_length/2 + splitter_length/2 + arm_length/2, waveguide_width/2 + splitter_length, 0))

upper_arm2 = mp.Block(material=mp.Medium(index=1.5),
                      size=mp.Vector3(arm_length, waveguide_width, mp.inf),
                      center=mp.Vector3(waveguide_length/2 - splitter_length/2 - arm_length/2, waveguide_width/2 + splitter_length, 0))

# Add the upper arm structures to the simulation cell
sim.geometry.append(upper_arm1)
sim.geometry.append(upper_arm2)

# Define the lower arm structures
lower_arm1 = mp.Block(material=mp.Medium(index=1.5),
                      size=mp.Vector3(arm_length, waveguide_width, mp.inf),
                      center=mp.Vector3(-waveguide_length/2 + splitter_length/2 + arm_length/2, -waveguide_width/2 - splitter_length, 0))

lower_arm2 = mp.Block(material=mp.Medium(index=1.5),
                      size=mp.Vector3(arm_length, waveguide_width, mp.inf),
                      center=mp.Vector3(waveguide_length/2 - splitter_length/2 - arm_length/2, -waveguide_width/2 - splitter_length, 0))

# Add the lower arm structures to the simulation cell
sim.geometry.append(lower_arm1)
sim.geometry.append(lower_arm2)

# Connect lower arms to Y splitter
lower_arm1_splitter = mp.Block(material=mp.Medium(index=1.5),
                               size=mp.Vector3(waveguide_width, splitter_length, mp.inf),
                               center=mp.Vector3(-waveguide_length/2 + splitter_length/2, -waveguide_width/2 - splitter_length/2, 0))

lower_arm2_splitter = mp.Block(material=mp.Medium(index=1.5),
                               size=mp.Vector3(waveguide_width, splitter_length, mp.inf),
                               center=mp.Vector3(waveguide_length/2 - splitter_length/2, -waveguide_width/2 - splitter_length/2, 0))

# Add the connections to the simulation cell
sim.geometry.append(lower_arm1_splitter)
sim.geometry.append(lower_arm2_splitter)

# Define the phase shifter structure
phase_shifter = mp.Block(material=mp.Medium(index=1.5),
                         size=mp.Vector3(phase_shifter_length, waveguide_width, mp.inf),
                         center=mp.Vector3(0, waveguide_width/2 + splitter_length + phase_shifter_length/2, 0))

# Add the phase shifter structure to the simulation cell
sim.geometry.append(phase_shifter)

# Set up the boundary conditions and run the simulation
sim.run(until=1)

# Plot the structure
eps_data = sim.get_array(center=mp.Vector3(), size=cell_size, component=mp.Dielectric)

plt.figure(figsize=(10, 6), dpi=100)
plt.imshow(np.flipud(np.transpose(eps_data)),
           cmap='binary',
           interpolation='spline36',
           extent=(-cell_size.x/2, cell_size.x/2, -cell_size.y/2, cell_size.y/2))

plt.xlabel('x')
plt.ylabel('y')
plt.title('Mach-Zehnder Interferometer Structure')
#plt.colorbar(label='Dielectric Constant')

plt.show()

