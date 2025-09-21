// Integrate N-body problem with springs between all bodies
#include "../include/dtypes.cuh"
#include "../include/inits.cuh"
#include "../include/polarity.cuh"
#include "../include/solvers.cuh"
#include "../include/vtk.cuh"
#include <string>


const auto r_c = 0.5f; // equilibrium distance
__device__ auto n_time_steps = 100u; // no. of time steps
__device__ double dt = 0.05f; // time step
__device__ int n_cells = 1000;
__device__ double a = 1.0f;
__device__ double r_max = 1.0f;

MAKE_PT(Cell, f);

__device__ Cell morse(Cell Xi, Cell r, float dist, int i, int j)
{
    Cell dF{0}; // 0 vector
    if (i == j) return dF; // if the two indeces are the same return the 0-vector
    if (dist > r_max) return dF; // if the distance is greater than the maximum interaction length it's also the 0 vector

    double F = 2 * (exp(-2*a*(dist - r_c)) - exp(-a*(dist - r_c))); // strength of the Morse potential
    if (F > 100) {
        printf("%f - %f", F, dist);
    }

    dF.x = F * r.x / dist;
    dF.y = F * r.y / dist;
    dF.z = F * r.z / dist;
    dF.f = F;
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
    n_time_steps = stoi(argv[5]);
    dt = stod(argv[6]);
    int every_n = stoi(argv[7]);

    // Prepare initial state
    Solution<Cell, Gabriel_solver> cells{n_cells};
    regular_rectangle(0.4f, rect, cells);

    // Integrate positions
    Vtk_output output{"out"}; 
    for (auto time_step = 0; time_step <= n_time_steps; time_step++) {
        cells.copy_to_host();
        cells.take_step<morse>(dt);    
        if(time_step % every_n == 0) {
            output.write_positions(cells);
            output.write_field(cells, "f", &Cell::f);
        }
    }

    return 0;
}
