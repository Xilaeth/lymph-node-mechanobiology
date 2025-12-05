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
__device__ double D = 0.0;
__device__ double force = 0.1;
__device__ double *fs;

MAKE_PT(Cell, f, fo);


__device__ Cell morse(Cell Xi, Cell r, float dist, int i, int j) {
    Cell dF{0}; // 0 vector

    // if i == j add random noise and external force
    if (i == j) {
        if (Xi.fo == 1) {
            dF.x = force;
        }
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
    fs[i] += F;
    return dF; 
}


// order of parameters is: n_cells, 
int main(int argc, const char* argv[])
{
    using namespace std;

    double a_temp = stod(argv[2]); 
    cudaMemcpyToSymbol(a, &a_temp, sizeof(double));
    double dt_temp = stod(argv[3]);
    cudaMemcpyToSymbol(dt, &dt_temp, sizeof(double));
    string file = argv[1]; 
    int n_time_steps = stoi(argv[4]);
    int every_n = stoi(argv[5]);
    double D_temp = stod(argv[6]);
    cudaMemcpyToSymbol(D, &D_temp, sizeof(double));
    double frac_temp = stod(argv[7]);
    cudaMemcpyToSymbol(frac, &frac_temp, sizeof(double));
    double force_temp = stod(argv[8]);
    cudaMemcpyToSymbol(force, &force_temp, sizeof(double));

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
        
    Vtk_input input{file};
    Solution<Cell, Gabriel_solver> cells{n_cells, 50, float(4*r_c*frac_temp)};

    input.read_positions(cells);
    input.read_field(cells, "fo", &Cell::fo);

    cells.copy_to_device();

    Vtk_output output{"out"};  
    for (auto time_step = 0; time_step <= n_time_steps; time_step++) {

        double fs_temp[n_cells];
        for (int i = 0; i <= n_cells; i++) {
            fs_temp[i] = 0;
        }
        double *d_tmp;
        cudaMalloc(&d_tmp, n_cells * sizeof(double));
        cudaMemcpy(d_tmp, fs_temp, n_cells * sizeof(double), cudaMemcpyHostToDevice);
        cudaMemcpyToSymbol(fs, &d_tmp, sizeof(double *));

        cudaDeviceSynchronize();
        cells.copy_to_host();
        cells.take_step<morse, friction_on_background>(dt_temp);    

        double *d_fs;
        cudaMemcpyFromSymbol(&d_fs, fs, sizeof(double*));
        cudaMemcpy(fs_temp, d_fs, n_cells * sizeof(double), cudaMemcpyDeviceToHost);
        for (int i = 0; i <= n_cells; i++) {
            cells.h_X[i].f = fs_temp[i];
        }

        if (time_step % every_n == 0) {
            output.write_positions(cells);  // use thread for full concurrency.
            output.write_field(cells, "f", &Cell::f);
            output.write_field(cells, "fo", &Cell::fo);
        }
    }

    return 0;
}
