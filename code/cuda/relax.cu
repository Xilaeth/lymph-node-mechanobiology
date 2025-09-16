// Integrate N-body problem with springs between all bodies
#include "../include/dtypes.cuh"
#include "../include/inits.cuh"
#include "../include/solvers.cuh"
#include "../include/vtk.cuh"


const auto r_max = 1.f; // maximum interaction length
const auto r_c = 0.5f; // equilibrium distance
const auto a = 1.f; // repulsion strength of the morse potential
const auto n_cells = 900u; // no. of bodies
const auto n_time_steps = 100u; // no. of time steps
const auto dt = 0.001f; // time step


__device__ float3 morse(float3 Xi, float3 r, float dist, int i, int j)
{
    float3 dF{0}; // 0 vector
    if (i == j) return dF; // if the two indeces are the same return the 0-vector
    if (dist > r_c) return dF; // if the distance is greater than the maximum interaction length it's also the 0 vector

    float F = 2 * (exp(-2*a*(dist - r_c)) - exp(-a*(dist - r_c))); // strength of the Morse potential

    dF = r * F / dist; // multiply it with the direction vector
    return dF; // return force that's to be applied
}


int main(int argc, const char* argv[])
{
    // Prepare initial state
    Solution<float3, Gabriel_solver> cells{n_bodies};
    random_sphere(0.4f, 30, cells);

    // Integrate positions
    Vtk_output output{"relax"};  // Writes to output/relax_#.vtk
    for (auto time_step = 0; time_step <= n_time_steps; time_step++) {
        cells.copy_to_host();
        cells.take_step<morse>(dt);    // Ordered to write during calculation,
        output.write_positions(cells);  // use thread for full concurrency.
    }

    return 0;
}
