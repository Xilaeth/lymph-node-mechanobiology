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
const auto r_c = 0.5f; 
__device__ double dt = 0.05f; 
__device__ double a = 0.2f;
__device__ double b = 0.01f;
__device__ double D = 0.0;
__device__ double *fs;
__device__ int ci = -1;
__device__ int ic = -1;

MAKE_PT(Cell, f, ct);

__device__ Cell morse(Cell Xi, Cell r, float dist, int i, int j) {
    Cell dF{0}; 

    if (Xi.ct == 1) {
        if (not(ic == i)) {
            ic = i;
            ci += 1;
        }
        if (i == j) {
            return dF;
        }

        double F = 0;
        if (not(r.ct == 0)) {
            if (dist <= 1) {
                F = b*(1 - 2*dist);
            }
        } else {
            if (dist <= r_c) {
                F = a*(1 - 2*dist);
            } else {
                F = a*(dist/frac - 2);
            }
        }

        dF.x = F * r.x / dist;
        dF.y = F * r.y / dist;
        dF.z = F * r.z / dist;
        fs[ci] += F;
    } else if (Xi.ct == 2) {
        if (i == j) {
            return dF;
        }

        double F = 0;
        if (not(r.ct == 0)) {
            if (dist <= r_c) {
                F = a*(1 - 2*dist);
            }
        } else {
            if (dist <= 1) {
                F = b*(1 - 2*dist);
            } 
        }

        dF.x = F * r.x / dist;
        dF.y = F * r.y / dist;
        dF.z = F * r.z / dist;
    }
    return dF;
}

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
    double b_temp = stod(argv[8]); 
    cudaMemcpyToSymbol(b, &b_temp, sizeof(double));
    int N = stoi(argv[9]); 

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
    input.read_field(cells, "ct", &Cell::ct);

    // NOT DONE
    int indeces[N];
    for (int i = 0; i < n_cells; i++) {
        if (cells.h_X[i].ct == 1) {

        }
    }

    cells.copy_to_device();

    Vtk_output output{"out"};  
    for (auto time_step = 0; time_step <= n_time_steps; time_step++) {
        cudaDeviceSynchronize();

        int init_ci = -1;
        cudaMemcpyToSymbol(ci, &init_ci, sizeof(int));

        double fs_temp[N];
        for (int i = 0; i < N; i++) {
            fs_temp[i] = 0;
        }
        double *d_tmp;
        cudaMalloc(&d_tmp, N * sizeof(double));
        cudaMemcpy(d_tmp, fs_temp, N * sizeof(double), cudaMemcpyHostToDevice);
        cudaMemcpyToSymbol(fs, &d_tmp, sizeof(double *));

        cells.copy_to_host();
        cells.take_step<morse, friction_on_background>(dt_temp);

        double *d_fs;
        cudaMemcpyFromSymbol(&d_fs, fs, sizeof(double*));
        cudaMemcpy(fs_temp, d_fs, N * sizeof(double), cudaMemcpyDeviceToHost);
        for (int i = 0; i < N; i++) {
            cells.h_X[i].f = fs_temp[i];
        }

        if (time_step % every_n == 0) {
            output.write_positions(cells);  
            output.write_field(cells, "f", &Cell::f);
            output.write_field(cells, "ct", &Cell::ct);
        }
    }

    return 0;
}
