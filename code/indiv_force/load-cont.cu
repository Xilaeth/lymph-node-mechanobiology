#include "../include/dtypes.cuh"
#include "../include/inits.cuh"
//#include "../include/solvers-modified.cuh"
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

const auto r_c = 0.5f; // equilibrium distance
__device__ double dt = 0.05f; // time step
__device__ double a = 1.0f;
__device__ double r_max = 1.0f;
__device__ double D = 0.0;
__device__ double f = 0.0;
__device__ int id = 0;
__device__ int f_dir = 0; // direction of the force

// new data type that stores force as well
MAKE_PT(Cell, v);

// random forces
__device__ Cell *dW;

__device__ Cell morse(Cell Xi, Cell r, float dist, int i, int j) {
    Cell dF{0}; // 0 vector

    // if i == j add random noise and external force
    if (i == j) {
        if (int(Xi.v) == id) {
            if (fdir == 1) {
                dF.x += f;
            } else if (fdir == 2) {
                dF.y += f;
            } else if (fdir == -1) {
                dF.x -= f;
            } else if (fdir == -2) {
                dF.y -= f;
            }

            /*
            switch (f_dir) {
                case 1:
                    dF.x += f;
                    break;
                case 2:
                    dF.y += f;
                    break;
                case 3:
                    dF.z += f;
                    break;
                case -1:
                    dF.x -= f;
                    break;
                case -2:
                    dF.y -= f;
                    break;
                case -3:
                    dF.z -= f;
                    break;
            }
            */
        }
        dF += dW[i];
        return dF;
    }

    if (dist > r_max) return dF; // if the distance is greater than the maximum interaction length it's also the 0 vector

    double F = 2 * (expf(-2*a*(dist - r_c)) - expf(-a*(dist - r_c))); // strength of the Morse potential

    dF.x = F * r.x / dist;
    dF.y = F * r.y / dist;
    dF.z = F * r.z / dist;
    return dF; // return force that's to be applied
}

// generate random forces
__global__ void generate_noise(int n, curandState* d_state) {
    // as we start the genrate_noise function we get the index by the thread of the call
    auto i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= n) return;

    dW[i].x = curand_normal(&d_state[i]) * powf(dt, 0.5) * D / dt;
    dW[i].y = curand_normal(&d_state[i]) * powf(dt, 0.5) * D / dt;
    dW[i].z = 0.0; //1*curand_normal(&d_state[i]) * powf(dt, 0.5) * D / dt;
    dW[i].v = 0.0;
}

// order of parameters is: n_cells, 
int main(int argc, const char* argv[])
{
    using namespace std;

    double a_temp = stod(argv[2]); // repulsion strength of the morse potential
    cudaMemcpyToSymbol(a, &a_temp, sizeof(double));
    double r_max_temp = stod(argv[3]); // repulsion strength of the morse potential
    cudaMemcpyToSymbol(r_max, &r_max_temp, sizeof(double));
    double dt_temp = stod(argv[5]);
    cudaMemcpyToSymbol(dt, &dt_temp, sizeof(double));
    string file = argv[1]; // input file name
    int n_time_steps = stoi(argv[4]);
    int every_n = stoi(argv[6]);
    double D_temp = stod(argv[7]);
    cudaMemcpyToSymbol(D, &D_temp, sizeof(double));
    double f_temp = stod(argv[8]);
    cudaMemcpyToSymbol(f, &f_temp, sizeof(double));
    int f_dir_temp = stoi(argv[9]);
    cudaMemcpyToSymbol(f_dir, &f_dir_temp, sizeof(int));

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
    Solution<Cell, Gabriel_solver> cells{n_cells};

    input.read_positions(cells);
    input.read_field(cells, "v", &Cell::v);

    // Prepare random state
    curandState* d_state;
    cudaMalloc(&d_state, n_cells*sizeof(curandState));
    auto seed = time(NULL);
    setup_rand_states<<<(n_cells + 32 - 1)/32, 32>>>(n_cells, seed, d_state);

    Property<Cell> W{n_cells, "wiener_process"};
    cudaMemcpyToSymbol(dW, &W.d_prop, sizeof(dW));

    double cells_init[n_cells][4];

    for (int i = 0; i < n_cells; i++) {
        cells_init[i][0] = cells.h_X[i].x;
        cells_init[i][1] = cells.h_X[i].y;
        cells_init[i][2] = cells.h_X[i].z;
        cells_init[i][3] = cells.h_X[i].v;
    }


    for (int i = 0; i < n_cells; i++) {
//        if (not(i % 100 == 0)) continue;
        cudaMemcpyToSymbol(id, &i, sizeof(int));

        for (int j = 0; j < n_cells; j++) {
            cells.h_X[j].x = cells_init[j][0];
            cells.h_X[j].y = cells_init[j][1];
            cells.h_X[j].z = cells_init[j][2];
            cells.h_X[j].v = cells_init[j][3];
        }

        cells.copy_to_device();

        string o = "out-";
        string ou = o + to_string(i);

        // Integrate positions
        Vtk_output output{ou};  // Writes to output/relax_#.vtk
        for (auto time_step = 0; time_step <= n_time_steps; time_step++) {
            cudaDeviceSynchronize();
            cells.copy_to_host();
            generate_noise<<<(n_cells + 32 - 1)/32, 32>>>(n_cells, d_state);
            cells.take_step<morse>(dt_temp);    // Ordered to write during calculation,
            if ((time_step % every_n) == 0) {
                output.write_positions(cells);  // use thread for full concurrency.
                output.write_field(cells, "v", &Cell::v);
            }
        }
    }

    return 0;
}
