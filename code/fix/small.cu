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
__device__ double b = 1.0f;
__device__ double D = 0.0;
__device__ double fo = 0.0;
__device__ int id = 0;
__device__ int f_dir = 0; // direction of the force

// new data type that stores force as well
MAKE_PT(Cell, v, f, ox, oy, oz);

// random forces
__device__ Cell *dW;

__device__ Cell morse(Cell Xi, Cell r, float dist, int i, int j) {
    Cell dF{0}; // 0 vector

    if (Xi.f == 1) {
        // if i == j add random noise and external force
        if (i == j) {
            if (Xi.v == id) {
                switch (f_dir) {
                    case 1:
                        dF.x += fo;
                        break;
                    case 2:
                        dF.y += fo;
                        break;
                    case 3:
                        dF.z += fo;
                        break;
                    case -1:
                        dF.x -= fo;
                        break;
                    case -2:
                        dF.y -= fo;
                        break;
                    case -3:
                        dF.z -= fo;
                        break;
                }
            }
            dF += dW[i];
            return dF;
        }

        if (not(0 == r.f)) {
            if (dist > r_c) return dF;

            double F = b*(1 - 2*dist);

            dF.x = F * r.x / dist;
            dF.y = F * r.y / dist;
            dF.z = F * r.z / dist;
            return dF; // return force that's to be applied
        }

        double F = 0;
        if (dist <= 1) {
            F = a*(1 - 2*dist);
        } else {
            F = a*(dist - 2);
        }

        dF.x = F * r.x / dist;
        dF.y = F * r.y / dist;
        dF.z = F * r.z / dist;
        return dF; // return force that's to be applied
    }

    if (Xi.f == 2) {
        if (i == j) return dF;
        if (dist > r_c) return dF;

        if (not(0 == r.f)) {
            double F = a*(1 - 2*dist);

            dF.x = F * r.x / dist;
            dF.y = F * r.y / dist;
            dF.z = F * r.z / dist;
            return dF; // return force that's to be applied
        }

        double F = b*(1 - 2*dist);

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
    dW[i].f = 0.0;
    dW[i].v = 0.0;
}

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
    double fo_temp = stod(argv[7]);
    cudaMemcpyToSymbol(fo, &fo_temp, sizeof(double));
    int f_dir_temp = stoi(argv[8]);
    cudaMemcpyToSymbol(f_dir, &f_dir_temp, sizeof(int));
    int n_real = stoi(argv[9]);
    double b_temp = stod(argv[10]);
    cudaMemcpyToSymbol(b, &b_temp, sizeof(double));

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
    Solution<Cell, Gabriel_solver> cells{n_cells, 50, 4*r_c};

    input.read_positions(cells);
    input.read_field(cells, "v", &Cell::v);
    input.read_field(cells, "f", &Cell::f);

    // Prepare random state
    curandState* d_state;
    cudaMalloc(&d_state, n_cells*sizeof(curandState));
    auto seed = time(NULL);
    setup_rand_states<<<(n_cells + 32 - 1)/32, 32>>>(n_cells, seed, d_state);

    Property<Cell> W{n_cells, "wiener_process"};
    cudaMemcpyToSymbol(dW, &W.d_prop, sizeof(dW));

    double cells_init[n_cells][5];
    double cells_out[n_real][3];
    int ind[n_real];
    int c = 0;

    for (int i = 0; i < n_cells; i++) {
        cells_init[i][0] = cells.h_X[i].x;
        cells_init[i][1] = cells.h_X[i].y;
        cells_init[i][2] = cells.h_X[i].z;
        cells_init[i][3] = cells.h_X[i].v;
        cells_init[i][4] = cells.h_X[i].f;
        if (cells_init[i][4] == 1) {
            ind[c] = i;
            c++;
        }
    }

    for (int i = 0; i < n_real; i++) {
        printf("%d / %d\n", i+1, n_real);
        cudaMemcpyToSymbol(id, &i, sizeof(int));


        for (int j = 0; j < n_cells; j++) {
            cells.h_X[j].x = cells_init[j][0];
            cells.h_X[j].y = cells_init[j][1];
            cells.h_X[j].z = cells_init[j][2];
            cells.h_X[j].v = cells_init[j][3];
            cells.h_X[j].f = cells_init[j][4];
        }

        cells.copy_to_device();

        // Integrate positions
        for (auto time_step = 0; time_step <= n_time_steps; time_step++) {
            cudaDeviceSynchronize();
            cells.copy_to_host();
            generate_noise<<<(n_cells + 32 - 1)/32, 32>>>(n_cells, d_state);
            cells.take_step<morse, friction_on_background>(dt_temp);    // Ordered to write during calculation,
        }
        cells_out[i][0] = cells.h_X[ind[i]].x - cells_init[ind[i]][0];
        cells_out[i][1] = cells.h_X[ind[i]].y - cells_init[ind[i]][1];
        cells_out[i][2] = cells.h_X[ind[i]].z - cells_init[ind[i]][2];
    }

    cells.copy_to_device();

    c = 0;
    for (int i = 0; i < n_cells; i++) {
        if (i == ind[c]) {
            cells.h_X[i].ox = cells_out[c][0];
            cells.h_X[i].oy = cells_out[c][1];
            cells.h_X[i].oz = cells_out[c][2];
            c++;
            continue;
        }
        cells.h_X[i].ox = 1000;
        cells.h_X[i].oy = 1000;
        cells.h_X[i].oz = 1000;
    }

    Vtk_output output{"out"};  // Writes to output/relax_#.vtk
    output.write_positions(cells);  // use thread for full concurrency.
    output.write_field(cells, "ox", &Cell::ox);
    output.write_field(cells, "oy", &Cell::oy);
    output.write_field(cells, "oz", &Cell::oz);

    return 0;
}
