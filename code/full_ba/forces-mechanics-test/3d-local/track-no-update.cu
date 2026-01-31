#include "../../../include/dtypes.cuh"
#include "../../../include/inits.cuh"
#include "../../../include/solvers-no-update.cuh"
#include "../../../include/vtk.cuh"
#include "../../../include/utils.cuh"
#include "../../../include/property.cuh"
#include <string>
#include <vector>
#include <fstream>
#include <sstream>
#include <cmath>
#include <stdio.h>

__device__ double dt = 0.05f; // time step
__device__ double a = 1.0f;
__device__ double b = 1.0f;
__device__ double d = 1.0f; // cut-off distance
__device__ double req = 1.0f; // equilibrium distance
__device__ double D = 0.0;
__device__ double f = 0.0;
__device__ int id = 0;
__device__ int f_dir = 0; // direction of the force

// new data type that stores force as well
MAKE_PT(Cell, v);

// random forces
__device__ Cell *dW;

__device__ Cell morse(Cell Xi, Cell r, float dist, int i, int j) {
    Cell dF{0}; 

    // these forces aren't counted in the force yet
    if (i == j) {
        if (int(Xi.v) == id) {
            switch (f_dir) {
                case 1:
                    dF.x += f;
                    break;
                case 2:
                    dF.y += f;
                    break;
                case -1:
                    dF.x -= f;
                    break;
                case -2:
                    dF.y -= f;
                    break;
            }
        }
        dF += dW[i];
        return dF;
    }

    double F = 0;
    if (dist <= b*req) {
        F = a*(1 - (dist/req));
    } else if (dist <= d) {
        F = a*((b-1)*( (dist - b*req)/(d - b*req)) + 1 - b);
    } else {
        F = 0;
    }

    dF.x = F * r.x / dist;
    dF.y = F * r.y / dist;
    dF.z = F * r.z / dist;
    return dF; // return force that's to be applied
}

__global__ void generate_noise(int n, curandState* d_state) {
    // as we start the genrate_noise function we get the index by the thread of the call
    auto i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= n) return;

    dW[i].x = curand_normal(&d_state[i]) * powf(dt, 0.5) * D / dt;
    dW[i].y = curand_normal(&d_state[i]) * powf(dt, 0.5) * D / dt;
    dW[i].z = 0.0; //1*curand_normal(&d_state[i]) * powf(dt, 0.5) * D / dt;
}


int main(int argc, const char* argv[])
{
    using namespace std;

    string file = argv[1]; 
    double a_temp = stod(argv[2]); 
    cudaMemcpyToSymbol(a, &a_temp, sizeof(double));
    double b_temp = stod(argv[3]); 
    cudaMemcpyToSymbol(b, &b_temp, sizeof(double));
    double d_temp = stod(argv[4]); 
    cudaMemcpyToSymbol(d, &d_temp, sizeof(double));
    double req_temp = stod(argv[5]); 
    cudaMemcpyToSymbol(req, &req_temp, sizeof(double));
    double dt_temp = stod(argv[6]);
    cudaMemcpyToSymbol(dt, &dt_temp, sizeof(double));
    int n_time_steps = stoi(argv[7]);
    int every_n = stoi(argv[8]);
    double D_temp = stod(argv[9]);
    cudaMemcpyToSymbol(D, &D_temp, sizeof(double));
    double f_temp = stod(argv[10]);
    cudaMemcpyToSymbol(f, &f_temp, sizeof(double));
    int f_dir_temp = stoi(argv[11]);
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
    Solution<Cell, Gabriel_solver> cells{n_cells, 100, float(d_temp)};

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

        Vtk_output output{ou};  
        for (auto time_step = 0; time_step <= n_time_steps; time_step++) {

            cudaDeviceSynchronize();
            cells.copy_to_host();
            generate_noise<<<(n_cells + 32 - 1)/32, 32>>>(n_cells, d_state);
            cells.take_step<morse, friction_on_background>(dt_temp);

            if ((time_step % every_n == 0) and (time_step != 0)) {
                output.write_positions(cells);  // use thread for full concurrency.
            }
        }
    }

    return 0;
}
