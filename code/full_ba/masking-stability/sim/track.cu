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
__device__ double *fsx;
__device__ double *fsy;

// new data type that stores force as well
MAKE_PT(Cell, fx, fy);

// random forces
__device__ Cell *dW;

__device__ Cell morse(Cell Xi, Cell r, float dist, int i, int j) {
    Cell dF{0}; 

    if (i == j) {
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
    fsx[i] += F * r.x / dist;
    fsy[i] += F * r.y / dist;
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
    dW[i].fx = 0.0;
    dW[i].fy = 0.0;
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

    // Prepare random state
    curandState* d_state;
    cudaMalloc(&d_state, n_cells*sizeof(curandState));
    auto seed = time(NULL);
    setup_rand_states<<<(n_cells + 32 - 1)/32, 32>>>(n_cells, seed, d_state);

    Property<Cell> W{n_cells, "wiener_process"};
    cudaMemcpyToSymbol(dW, &W.d_prop, sizeof(dW));

    cells.copy_to_device();

    Vtk_output output{"out"};  
    for (auto time_step = 0; time_step <= n_time_steps; time_step++) {

        double fsx_temp[n_cells];
        double fsy_temp[n_cells];
        for (int i = 0; i < n_cells; i++) {
            fsx_temp[i] = 0;
            fsy_temp[i] = 0;
        }
        double *dx_tmp;
        cudaMalloc(&dx_tmp, n_cells * sizeof(double));
        cudaMemcpy(dx_tmp, fsx_temp, n_cells * sizeof(double), cudaMemcpyHostToDevice);
        cudaMemcpyToSymbol(fsx, &dx_tmp, sizeof(double *));
        double *dy_tmp;
        cudaMalloc(&dy_tmp, n_cells * sizeof(double));
        cudaMemcpy(dy_tmp, fsy_temp, n_cells * sizeof(double), cudaMemcpyHostToDevice);
        cudaMemcpyToSymbol(fsy, &dy_tmp, sizeof(double *));

        cudaDeviceSynchronize();
        cells.copy_to_host();
        generate_noise<<<(n_cells + 32 - 1)/32, 32>>>(n_cells, d_state);
        cells.take_step<morse, friction_on_background>(dt_temp);

        double *d_fsx;
        cudaMemcpyFromSymbol(&d_fsx, fsx, sizeof(double*));
        cudaMemcpy(fsx_temp, d_fsx, n_cells * sizeof(double), cudaMemcpyDeviceToHost);
        double *d_fsy;
        cudaMemcpyFromSymbol(&d_fsy, fsy, sizeof(double*));
        cudaMemcpy(fsy_temp, d_fsy, n_cells * sizeof(double), cudaMemcpyDeviceToHost);
        for (int i = 0; i < n_cells; i++) {
            cells.h_X[i].fx = fsx_temp[i];
            cells.h_X[i].fy = fsy_temp[i];
        }

        if (time_step % every_n == 0) {
            output.write_positions(cells);  // use thread for full concurrency.
            output.write_field(cells, "fx", &Cell::fx);
            output.write_field(cells, "fy", &Cell::fy);
        }
        cudaFree(d_fsx);
        cudaFree(d_fsy);
        cudaFree(dx_tmp);
        cudaFree(dy_tmp);
    }

    return 0;
}
