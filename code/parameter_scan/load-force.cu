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

const auto r_c = 0.5f; // equilibrium distance
__device__ double dt = 0.05f; // time step
__device__ double a = 1.0f;
__device__ double a2 = 1.0f;
__device__ double r_max = 1.0f;
__device__ double D = 0.0;
__device__ double fxl = 0.0;
__device__ double fxr = 0.0;
__device__ double fyu = 0.0;
__device__ double fyd = 0.0;
__device__ double fxyur = 0.0;
__device__ double fxyul = 0.0;
__device__ double fxydr = 0.0;
__device__ double fxydl = 0.0;

// new data type that stores force as well
MAKE_PT(Cell, v, vf);

// random forces
__device__ Cell *dW;

__device__ Cell morse(Cell Xi, Cell r, float dist, int i, int j) {
    Cell dF{0}; // 0 vector

    if (Xi.v == 1) {
        if (i == j) {
            switch (int(Xi.vf)) {
                case 1:
                    dF.x -= fxl;
                    break;
                case 2:
                    dF.y += fyu;
                    break;
                case 3:
                    dF.x += fxr;
                    break;
                case 4:
                    dF.y -= fyd;
                    break;
                case 5:
                    dF.x -= 0.7071*fxydl;
                    dF.y -= 0.7071*fxydl;
                    break;
                case 6:
                    dF.x -= 0.7071*fxyul;
                    dF.y += 0.7071*fxyul;
                    break;
                case 7:
                    dF.x += 0.7071*fxyur;
                    dF.y += 0.7071*fxyur;
                    break;
                case 8:
                    dF.x += 0.7071*fxydr;
                    dF.y -= 0.7071*fxydr;
                    break;
            }
            dF += dW[i];
            return dF;
        }

        if ((r.v != 0) && (dist > r_c)) return dF;

        if (dist > r_max) return dF; // if the distance is greater than the maximum interaction length it's also the 0 vector

        double F = 2 * (exp(-2*a*(dist - r_c)) - exp(-a*(dist - r_c))); // strength of the Morse potential

        dF.x = F * r.x / dist;
        dF.y = F * r.y / dist;
        dF.z = F * r.z / dist;
        return dF; // return force that's to be applied
    }

    if (Xi.v == 2) {
        if (i == j) return dF;
        if (dist > r_c) return dF; // only repulsive forces

        double F = 2 * (exp(-2*a2*(dist - r_c)) - exp(-a2*(dist - r_c))); // strength of the Morse potential

        dF.x = F * r.x / dist;
        dF.y = F * r.y / dist;
        dF.z = F * r.z / dist;
        return dF; // return force that's to be applied
    }

    return dF;
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
    double a2_temp = stod(argv[3]); // repulsion strength of the morse potential
    cudaMemcpyToSymbol(a2, &a2_temp, sizeof(double));
    double r_max_temp = stod(argv[4]); // repulsion strength of the morse potential
    cudaMemcpyToSymbol(r_max, &r_max_temp, sizeof(double));
    double dt_temp = stod(argv[6]);
    cudaMemcpyToSymbol(dt, &dt_temp, sizeof(double));
    string file = argv[1]; // input file name
    int n_time_steps = stoi(argv[5]);
    int every_n = stoi(argv[7]);
    double D_temp = stod(argv[8]);
    cudaMemcpyToSymbol(D, &D_temp, sizeof(double));
    double fxr_temp = stod(argv[9]);
    cudaMemcpyToSymbol(fxr, &fxr_temp, sizeof(double));
    double fxl_temp = stod(argv[10]);
    cudaMemcpyToSymbol(fxl, &fxl_temp, sizeof(double));
    double fyu_temp = stod(argv[11]);
    cudaMemcpyToSymbol(fyu, &fyu_temp, sizeof(double));
    double fyd_temp = stod(argv[12]);
    cudaMemcpyToSymbol(fyd, &fyd_temp, sizeof(double));
    double fxyur_temp = stod(argv[13]);
    cudaMemcpyToSymbol(fxyur, &fxyur_temp, sizeof(double));
    double fxyul_temp = stod(argv[14]);
    cudaMemcpyToSymbol(fxyul, &fxyul_temp, sizeof(double));
    double fxydr_temp = stod(argv[15]);
    cudaMemcpyToSymbol(fxydr, &fxydr_temp, sizeof(double));
    double fxydl_temp = stod(argv[16]);
    cudaMemcpyToSymbol(fxydl, &fxydl_temp, sizeof(double));

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
    input.read_field(cells, "vf", &Cell::vf);
    cells.copy_to_device();

    // Prepare random state
    curandState* d_state;
    cudaMalloc(&d_state, n_cells*sizeof(curandState));
    auto seed = time(NULL);
    setup_rand_states<<<(n_cells + 32 - 1)/32, 32>>>(n_cells, seed, d_state);

    Property<Cell> W{n_cells, "wiener_process"};
    cudaMemcpyToSymbol(dW, &W.d_prop, sizeof(dW));

    // Integrate positions
    Vtk_output output{"out"};  // Writes to output/relax_#.vtk
    for (auto time_step = 0; time_step <= n_time_steps; time_step++) {
        cudaDeviceSynchronize();
        cells.copy_to_host();
        generate_noise<<<(n_cells + 32 - 1)/32, 32>>>(n_cells, d_state);
        cells.take_step<morse>(dt_temp);    // Ordered to write during calculation,
        if ((time_step % every_n) == 0) {
            output.write_positions(cells);  // use thread for full concurrency.
            output.write_field(cells, "vf", &Cell::vf);
            output.write_field(cells, "v", &Cell::v);
        }
    }

    return 0;
}
