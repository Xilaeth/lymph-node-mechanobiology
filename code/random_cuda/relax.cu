#include "../include/dtypes.cuh"
#include "../include/inits.cuh"
#include "../include/solvers.cuh"
#include "../include/vtk.cuh"
#include "../include/utils.cuh"
#include "../include/property.cuh"

#include <string>
#include <stdio.h>


const auto r_c = 0.5f; // equilibrium distance
auto n_time_steps = 100u; // no. of time steps
__device__ double dt = 0.05f; // time step
int n_cells = 1000;
__device__ double a = 5.0f;
__device__ double r_max = 1.0f;
__device__ double D = 0.0f;

// new data type that stores force as well
MAKE_PT(Cell, f);

// random forces
__device__ Cell *dW;


__device__ Cell morse(Cell Xi, Cell r, float dist, int i, int j)
{
    Cell dF{0}; // 0 vector

    // if i == j add random noise
    if (i == j) {
       dF += dW[i];
       return dF;
    }

    if (dist > r_max) return dF; // if the distance is greater than the maximum interaction length it's also the 0 vector

    double F = 2 * (exp(-2*a*(dist - r_c)) - exp(-a*(dist - r_c))); // strength of the Morse potential

    dF.x = F * r.x / dist;
    dF.y = F * r.y / dist;
    dF.z = F * r.z / dist;
    dF.f = F/dt;
    return dF; // return force that's to be applied
}

// generate random forces
__global__ void generate_noise(int n, curandState* d_state) {
    // as we start the genrate_noise function we get the index by the thread of the call
    auto i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= n) return;

    dW[i].x = curand_normal(&d_state[i]) * powf(dt, 0.5) * D / dt;
    dW[i].y = curand_normal(&d_state[i]) * powf(dt, 0.5) * D / dt;
    dW[i].z = 0.0; //powf(dt, 0.5) * D / dt;
    dW[i].f = 0.0;
}

// the order of input parameters is: n_cells, a, sigma
int main(int argc, const char* argv[])
{
    using namespace std;

    n_cells = stoi(argv[1]); // no. of bodies
    double a_temp = stod(argv[2]); // repulsion strength of the morse potential
    cudaMemcpyToSymbol(a, &a_temp, sizeof(double));
    double r_max_temp = stod(argv[3]); // repulsion strength of the morse potential
    cudaMemcpyToSymbol(r_max, &r_max_temp, sizeof(double));
    double dt_temp = stod(argv[6]);
    cudaMemcpyToSymbol(dt, &dt_temp, sizeof(double));
    int rect = stoi(argv[4]);
    n_time_steps = stoi(argv[5]);
    int every_n = stoi(argv[7]);
    double starting_dist = stod(argv[8]);
    double D_temp = stod(argv[9]);
    cudaMemcpyToSymbol(D, &D_temp, sizeof(double));

    // Prepare initial state
    Solution<Cell, Gabriel_solver> cells{n_cells};
    regular_rectangle(starting_dist, rect, cells);

    // set up random states
    curandState* d_state;
    cudaMalloc(&d_state, n_cells*sizeof(curandState));
    auto seed = time(NULL);
    setup_rand_states<<<(n_cells + 32 - 1)/32, 32>>>(n_cells, seed, d_state);

    Property<Cell> W{n_cells, "wiener_process"};
    cudaMemcpyToSymbol(dW, &W.d_prop, sizeof(dW));

    // Integrate positions
    Vtk_output output{"out"}; 
    for (auto time_step = 0; time_step <= n_time_steps; time_step++) {
        cells.copy_to_host();
        generate_noise<<<(n_cells + 32 - 1)/32, 32>>>(n_cells, d_state);
        cells.take_step<morse, friction_w_neighbour>(dt_temp);    
        if(time_step % every_n == 0) {
            output.write_positions(cells);
            output.write_field(cells, "f", &Cell::f);
        }
    }

    return 0;
}
