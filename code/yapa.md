# This is a pesonal documentation of the ya||a library

## Files and their content

### cudebug.cuh
- seems to be unimportant for me

### dtypes.cuh
- seems to be defining how the float3, float4 and PT data types behaves in regards to already established operators in cpp

### inits.cuh
- this file defines all the implemented initial conditions for our cells
- `random_disk(float dist_to_nb, Solution& points)`
- `random_sphere(float dist_to_nb, Solution& points)`
- `random_cuboid(float dist_to_nb, float3 minimum, float3 maximum, Solution& points)`
- `regular_hexagon(float dist_to_nb, Solution& points)`
- `regular_rectangle(float dist_to_nb, int nx, Solution& points)`

### links.cuh
- seems to be about forces and walls, nothing that I am actively dealing with right now

### mesh.cuh
- seems to be about comparing an image with the points of a cell. Could become important later on but I don't wanna get into it too much right now

### polarity.cuh
- I won't have to work with polarity so I am skipping this file

### property.cuh
- seems to be some technical stuff that's not all that important to me

### solver.cuh
- this defines the different kinds of solvers
- `Tile_solver`
- `Grid_solver`
- `Gabriel_solver`

### utils.cuh
- doesn't seem important to me, once again technical stuff

### vtk.cuh
- defines how the data is saved to adhere to the vtk file format

## General structure of a program

- First we define the parameters that are important to us
- We then define a __device__ (runs on the GPU) of type float3 that takes the following input parameters: a float 3 (the current point we're looking at), a float3 (the difference of another cell and this cell), a float (the distance of the previous float3), int, int (the indeces of the current and other cell)
- In this device we define how exactly the force acts between two different cells in our system

- We then have a main function that has the following general structure
- We define a Solution<float3, Gabriel_solver> name{num of cells};
- We define the inital condition initialcondition(..., Solution);
- We define the vtk output namescheme: `Vtk_output output{"name"};`
- We loop over the time steps and do the following in the loop: we copy the cell to the host (`cells.copy_to_host();`); we take a step with our force function (`cells.take_step<force>(time step);`; we write the state to the output (`output.write_positions(cells);`)

## Things I learned over time
- generally in CUDA variables are split into device and host variables
- to load a device variable to the host or the other way around we use cudaMemcpyToSymbol
- The noise isn't automatically added in in ya||a, we therefore have to add it ourselves using curand (cuda random) variables that are created in parallel on the GPU
- We can create new POINT classes that have more parameters that we can write and read from files using the write/read_field function
- To apply forces to specific points is easiest by giving them a type and then applying the force to that type of cell
