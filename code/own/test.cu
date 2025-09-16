// Integrate N-body problem with springs between all bodies
#include "../include/dtypes.cuh"
#include "../include/inits.cuh"
#include "../include/solvers.cuh"
#include "../include/vtk.cuh"


const auto L_0 = 0.5f;  // Relaxed spring length
const auto n_bodies = 800u; // no. of bodies
const auto n_time_steps = 100u; // no. of time steps
const auto dt = 0.001f; // time step


__device__ float3 spring(float3 Xi, float3 r, float dist, int i, int j)
{
    float3 dF{0}; // 0 vector
    if (i == j) return dF; // if the two indeces are the same return the 0-vector

    dF = r * (L_0 - dist) / dist; // change in the force equals the direction "r" times Hook's law
    return dF; // return force that's to be applied
}


int main(int argc, const char* argv[])
{
    // Prepare initial state
    Solution<float3, Tile_solver> bodies{n_bodies};
    random_sphere(L_0, bodies);

    // Integrate positions
    Vtk_output output{"springs"};  // Writes to output/springs_#.vtk
    for (auto time_step = 0; time_step <= n_time_steps; time_step++) {
        bodies.copy_to_host();
        bodies.take_step<spring>(dt);    // Ordered to write during calculation,
        output.write_positions(bodies);  // use thread for full concurrency.
    }

    return 0;
}
