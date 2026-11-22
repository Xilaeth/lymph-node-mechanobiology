# Computational Simulation of the Ising Model

This project implements a pipeline that turns three-dimensional confocal microscopy data of the actin structures in
human lymph nodes into agent-based cell structures to infer mechanobiological properties such as their elasticity.

This project served as my BSc thesis for the Physics Bachelor at the Goethe University Frankfurt. The thesis was written
in collaboration with the Matthaeus Group at the Frankfurt Institute for Advanced Studies (FIAS) and used data from the
Martin-Leo Hansmann group at the University Clinic Frankfurt and the FIAS. 

> **Status:** Archived academic project - cleaned up for reference

## Features
- Includes the Python code necessary to turn the TIFF stacks into the `.vtk` format which is then used to initialize the simulation.
- Includes the CUDA code to run the simulation and mechanical inference.
- Includes the Python code for the statistical analysis of the results.

## Prerequisites

- **Python:** 3.8+ 
- **FFMPEG**
- **Libraries:**
    - **Numpy** 
    - **matplotlib** 
    - **vedo**
    - **tifffile**

## Getting Started

You can inspect the code in the `code/` folder and run the individual modules.

For an overview of the projects, the theoretical background and the results you can check out the accompanying presentation in `slides.pdf`.
