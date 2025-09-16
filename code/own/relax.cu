// Integrate N-body problem with springs between all bodies
#include "../include/dtypes.cuh"
#include "../include/inits.cuh"
#include "../include/solvers.cuh"
#include "../include/vtk.cuh"


const auto r_max = 1.0; // maximum interaction distance
const auto r_0 = 0.5; // equilibrium distance
const auto a = 1.0; // the strength of the morse potential
const auto num_cells = 900u; // no. of cells
const auto n_time_steps = 100u; // no. of time steps
const auto dt = 0.001f; // time step


__device__ float3 spring(float3 Xi, float3 r, float dist, int i, int j) // __device__ means it is compiled for execution on the GPU
{
    float3 dF{0}; // 0 vector
    if (i == j) return dF; // if the two indeces are the same return the 0-vector
    if (dist > r_max) return dF; // if the distance is greater than the maximum interaction distance return 0

    float F = 2 * (exp(-2 * a * (dist - r_0)) - exp(-a * (dist - r_0))); // calculates the magnitutde of the morse potential

    dF = r * F / dist; // defines the 3 vector with that magnitude

    return dF; // return force that's to be applied
}


int main(int argc, const char* argv[]) // main function with command line arguments
{
    // Prepare initial state
    Solution<float3, Grabriel_solver> cells{num_cells}; // Creates a solution class with the parameters float3, Gabriel solver with the name bodies and the 
//    random_sphere(L_0, bodies); // creates a sphere of length L_0 for the beads
    regular_rectangle(L_0, 30, cells); // should create a rectangle with 30 x 30 cells

    // Integrate positions
    Vtk_output output{"relax"};  // Writes to output/relax_#.vtk
    for (auto time_step = 0; time_step <= n_time_steps; time_step++) {
        bodies.copy_to_host();
        bodies.take_step<spring>(dt);    // Ordered to write during calculation,
        output.write_positions(bodies);  // use thread for full concurrency.
    }

    return 0;
}
