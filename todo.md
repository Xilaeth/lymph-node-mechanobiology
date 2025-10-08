# Todo
- [ ] Update the slide to include all the structured stuff
- [ ] Run a 3D simulation with a rescaled 3d file
- [ ] Check the stability of the 3d file
- [ ] Apply forces to the 3d file
- [ ] Write a script that checks the elasticity in the way that Franzi wanted it to be checked
- [ ] Figure out how to model a Coarse Grained Model of water using the Morse-Potential and checking parameters like "Diffusion", "Thermal Conductivity" and so on
- [ ] Maybe try to look up general elasticities for reticular networks that are similar
- [ ] Research Elastic Properties of Collagen Fibers
- [ ] Test models for the fibers on the computer and find parameters that fit best
- [ ] Calculate Stress-Strain curves for different parameters

# Doing
- [ ] Write a legend for the scripts and their usage

# Done
- [x] Write a better visualization of 3d files
- [x] Write a script that automatically does a parameter scan and quantizes the effect of the forces
- [x] Write a program that automatically quantifies the parameter scan (stretching parameter as the distance between the two most left/ right points over the initial size of the tissue)
- [x] Do a parameter scan with adjusted forces
- [x] Write resolution adjuster for tiff stacks
- [x] Do some research on Dissipative Particle Dynamics
- [x] Compare the elasticity of no change, no gabriel updater and inbetween
- [x] Run a first 3d simulation to have an example of what it could look like
- [x] Write script to subsample from the tif images and stacks
- [x] Write auto-mask script for the 3d tif files
- [x] Write code that compares the states and computes a linear response
- [x] Write script that checks a lot of different parameters for the input to see what is stable and what isn't using averages and stochasticity
- [x] Write a version of the solver with a second kind of repulsive bead
- [x] Figure out how to turn off Gabriel Updater in ya||a
- [x] Look at the file format of vtk that ya||a uses
- [x] Map out the structure of the ya||a library a bit
- [x] Uniform relaxed tissue using ya||a
- [x] implement the mask in python
- [x] Look at some examples of the vedo library and understand the general structure of it
- [x] Figuring out the mask from the vtk file
- [x] Find/ Make some bitmaps
- [x] Test out the masked tool to relax in cpp
- [x] Rewrite the density generating code in cpp for performance
- [x] write script that automatically determines the size and then applies a mask accordingly
- [x] check how long running 1000 time steps takes on my machine for different bead numbers
- [x] add stochasticity
- [x] flip the mask in python
- [x] hold the very edge states in place
- [x] Figure out tif files in 3d
- [x] Figure out how friction forces work in ya||a
- [x] Write script that creates 3d and 2d relaxed vtk files with a certain number of points 
- [x] Write code that takes the average of multiple simulations
- [x] Write code that takes in positions and gives out positions plus cell types
- [x] Write code that adds forces in a given direction with a certain magnitude
