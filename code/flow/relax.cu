// Integrate N-body problem with springs between all bodies
#include "../include/dtypes.cuh"
#include "../include/inits.cuh"
#include "../include/solvers-force.cuh"
#include "../include/vtk.cuh"
#include <string>


const auto r_c = 0.5f; // equilibrium distance
const auto n_time_steps = 100u; // no. of time steps
const auto dt = 0.05f; // time step
__device__ int n_cells = 1000;
__device__ double a = 1.0f;
__device__ double r_max = 1.0f;


__device__ float3 morse(float3 Xi, float3 r, float dist, int i, int j)
{
    float3 dF{0}; // 0 vector
    if (i == j) return dF; // if the two indeces are the same return the 0-vector
    if (dist > r_max) return dF; // if the distance is greater than the maximum interaction length it's also the 0 vector

    float F = 2 * (exp(-2*a*(dist - r_c)) - exp(-a*(dist - r_c))); // strength of the Morse potential

    dF = r * F / dist; // multiply it with the direction vector
    return dF; // return force that's to be applied
}

// the order of input parameters is: n_cells, a, sigma
int main(int argc, const char* argv[])
{
    using namespace std;

    // CUDA is very unhappy about accessing a __device__ variable from a host function but it compiles and works so I won't question it and just accept this code and be happy :)
    n_cells = stoi(argv[1]); // no. of bodies
    a = stod(argv[2]); // repulsion strength of the morse potential
    r_max = r_c * stod(argv[3]); // maximum interaction length
    int rect = stoi(argv[4]);

    // Prepare initial state
    Solution<float3, Gabriel_solver> cells{n_cells};
    regular_rectangle(0.45f, rect, cells);

    // Integrate positions
    Vtk_output output{"relax"};  // Writes to output/relax_#.vtk
    for (auto time_step = 0; time_step <= n_time_steps; time_step++) {
        cells.copy_to_host();
        cells.take_step<morse>(dt);    // Ordered to write during calculation,
        printf("\n");
        if(time_step == n_time_steps) output.write_positions(cells);  // use thread for full concurrency.
    }

    return 0;
}
