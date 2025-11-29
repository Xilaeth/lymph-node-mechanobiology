#include "../include/dtypes.cuh"
#include "../include/inits.cuh"
#include "../include/solvers.cuh"
#include "../include/vtk.cuh"
#include "../include/utils.cuh"
#include "../include/property.cuh"
#include <string>
#include <vector>
#include <fstream>
#include <sstream>
#include <cmath>
#include <stdio.h>

__device__ double frac = 1.0f;
const auto r_c = 0.5f; // equilibrium distance
__device__ double dt = 0.05f; // time step
__device__ double a = 1.0f;
__device__ double b = 1.0f;
__device__ double D = 0.0;
__device__ int id = 0;

// new data type that stores force as well
MAKE_PT(Cell, f);

// random forces
//__device__ Cell *dW;

__device__ Cell morse(Cell Xi, Cell r, float dist, int i, int j) {
    Cell dF{0}; // 0 vector

    // if i == j add random noise and external force
    if (i == j) {
//        dF += dW[i];
        return dF;
    }


    double F = 0;
    if (dist <= 1) {
        F = a*(1 - 2*dist);
    } else {
        F = a*(dist/frac - 2);
    }

    dF.x = F * r.x / dist;
    dF.y = F * r.y / dist;
    dF.z = F * r.z / dist;
    return dF; // return force that's to be applied
}

// generate random forces
/*
__global__ void generate_noise(int n, curandState* d_state) {
    // as we start the genrate_noise function we get the index by the thread of the call
    auto i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= n) return;

    dW[i].x = curand_normal(&d_state[i]) * powf(dt, 0.5) * D / dt;
    dW[i].y = curand_normal(&d_state[i]) * powf(dt, 0.5) * D / dt;
    dW[i].z = 0.0; //1*curand_normal(&d_state[i]) * powf(dt, 0.5) * D / dt;
    dW[i].f = 0.0;
}
*/

// order of parameters is: n_cells, 
int main(int argc, const char* argv[])
{
    using namespace std;

    double a_temp = stod(argv[2]); // repulsion strength of the morse potential
    cudaMemcpyToSymbol(a, &a_temp, sizeof(double));
    double dt_temp = stod(argv[3]);
    cudaMemcpyToSymbol(dt, &dt_temp, sizeof(double));
    string file = argv[1]; // input file name
    int n_time_steps = stoi(argv[4]);
    int every_n = stoi(argv[5]);
    double D_temp = stod(argv[6]);
    cudaMemcpyToSymbol(D, &D_temp, sizeof(double));
    double b_temp = stod(argv[7]);
    cudaMemcpyToSymbol(b, &b_temp, sizeof(double));
    double frac_temp = stod(argv[8]);
    cudaMemcpyToSymbol(frac, &frac_temp, sizeof(double));

    ifstream inp(file);

    string line;
    vector<string> content;
    int counter = 0;
    while(getline(inp, line)) {
        if (counter > 5) break;
        content.push_back(line);
        counter++;
    }
    auto l = content[5];
    vector<string> coords; 
    stringstream ss(l);
    string temp;
    while(ss >> temp) {
        coords.push_back(temp);
    }
    const int n_cells = stoi(coords[1]);
        
    // Prepare initial state
    Vtk_input input{file};
    Solution<Cell, Gabriel_solver> cells{n_cells, 50, float(4*r_c*frac_temp)};

    input.read_positions(cells);

    // Prepare random state
//    curandState* d_state;
//    cudaMalloc(&d_state, n_cells*sizeof(curandState));
//    auto seed = time(NULL);
//    setup_rand_states<<<(n_cells + 32 - 1)/32, 32>>>(n_cells, seed, d_state);

//    Property<Cell> W{n_cells, "wiener_process"};
//    cudaMemcpyToSymbol(dW, &W.d_prop, sizeof(dW));

    cells.copy_to_device();

    // Integrate positions
    Vtk_output output{"out"};  // Writes to output/relax_#.vtk
    for (auto time_step = 0; time_step <= n_time_steps; time_step++) {
        cudaDeviceSynchronize();
        cells.copy_to_host();
//        generate_noise<<<(n_cells + 32 - 1)/32, 32>>>(n_cells, d_state);
        cells.take_step<morse, friction_on_background>(dt_temp);    // Ordered to write during calculation,
        output.write_positions(cells);  // use thread for full concurrency.
        output.write_field(cells, "f", &Cell::f);
    }

    return 0;
}
