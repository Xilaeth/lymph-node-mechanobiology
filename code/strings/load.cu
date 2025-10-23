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
__device__ float dt = 0.05f; // time step
__device__ float a = 1.0f;
__device__ float r_max = 1.0f;
__device__ float D = 0.0;
__device__ float f = 0.0;
__device__ float F_0 = 1.0;

// new data type that stores force as well
MAKE_PT(Cell, v);

// random forces
__device__ Cell *dW;

__device__ Cell morse(Cell Xi, Cell r, float dist, int i, int j) {
    Cell dF{0}; // 0 vector
//    if (int(Xi.v) == -1) return dF;

    // if i == j add random noise and external force
    if (i == j) {
        switch (int(Xi.v)) {
            case 1:
                dF.y += f;
                break;
            case 2:
                dF.x += f;
                break;
        }
//        dF += dW[i];
        return dF;
    }


    if (dist > r_max) return dF; // if the distance is greater than the maximum interaction length it's also the 0 vector

    double F = 2 * a * F_0 * (expf(-2*a*(dist - r_c)) - expf(-a*(dist - r_c))); // strength of the Morse potential

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

    float a_temp = stof(argv[2]); // repulsion strength of the morse potential
    cudaMemcpyToSymbol(a, &a_temp, sizeof(float));
    float r_max_temp = stof(argv[3]); // repulsion strength of the morse potential
    cudaMemcpyToSymbol(r_max, &r_max_temp, sizeof(float));
    float dt_temp = stof(argv[5]);
    cudaMemcpyToSymbol(dt, &dt_temp, sizeof(float));
    string file = argv[1]; // input file name
    int n_time_steps = stoi(argv[4]);
    int every_n = stoi(argv[6]);
    float F_temp = stof(argv[7]);
    cudaMemcpyToSymbol(F_0, &F_temp, sizeof(float));
    float f_temp = stof(argv[8]);
    cudaMemcpyToSymbol(f, &f_temp, sizeof(float));

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
    cells.copy_to_device();

    int c = 0;

    for (int i = 0; i < n_cells; i++) {
        if (cells.h_X[i].v > 0) c++;
    }

    float cells_stat[c][4];

    int j = 0;
    for (int i = 0; i < n_cells; i++) {
        if (cells.h_X[i].v > 0) {
            cells_stat[j][0] = i;
            cells_stat[j][1] = cells.h_X[i].x;
            cells_stat[j][2] = cells.h_X[i].y;
            cells_stat[j][3] = cells.h_X[i].z;
            j++;
        }
    }

    float lx = cells.h_X[n_cells - 1].x - cells.h_X[0].x;
    float ly = cells.h_X[n_cells - 1].y - cells.h_X[0].y;

    // Prepare random state
    //curandState* d_state;
    //cudaMalloc(&d_state, n_cells*sizeof(curandState));
    //auto seed = time(NULL);
    //setup_rand_states<<<(n_cells + 32 - 1)/32, 32>>>(n_cells, seed, d_state);

    //Property<Cell> W{n_cells, "wiener_process"};
    //cudaMemcpyToSymbol(dW, &W.d_prop, sizeof(dW));

    // Integrate positions
    Vtk_output output{"out"};  // Writes to output/relax_#.vtk
    for (auto time_step = 0; time_step <= n_time_steps; time_step++) {
        cudaDeviceSynchronize();
        cells.copy_to_host();

        for (int i = 0; i < c; i++) {
            cells.h_X[int(cells_stat[i][0])].x = cells_stat[i][1];
            cells.h_X[int(cells_stat[i][0])].y = cells_stat[i][2];
            cells.h_X[int(cells_stat[i][0])].z = cells_stat[i][3];
        }

        float max_y = cells.h_X[n_cells - 1].y;
        float min_y = cells.h_X[0].y; 
        float max_x = cells.h_X[n_cells - 1].x; 
        float min_x = cells.h_X[0].x; 

        if ((max_x - min_x) > 3*lx) break;
        if ((max_y - min_y) > 3*ly) break;
    //    generate_noise<<<(n_cells + 32 - 1)/32, 32>>>(n_cells, d_state);
        cells.take_step<morse>(dt_temp);    // Ordered to write during calculation,
        if ((time_step % every_n) == 0) {
            output.write_positions(cells);  // use thread for full concurrency.
            output.write_field(cells, "v", &Cell::v);
        }
    }

    return 0;
}
