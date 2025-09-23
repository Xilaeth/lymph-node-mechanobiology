#include "./include/dtypes.cuh"
#include "./include/inits.cuh"
#include "./include/solvers.cuh"
#include "./include/vtk.cuh"
#include "./include/property.cuh"
#include "./include/utils.cuh"

#include <stdio.h>

const float r_max = 1.0;
const int n_cells = 1000;
const float dt = 0.1;
const int tMax = 500;

MAKE_PT(Cell, r);

__device__ Cell *d_W;
__device__ float3 *d_surface, *d_normals;
__device__ int *d_num_neighs;
__device__ float *d_forces_mechanical, *d_forces_surface;


__device__ Cell force_function(Cell Xi, Cell r, float dist, int i, int j) {
    Cell dF{0};

    //Sollbruchstelle
    if ((i==549) || (j==549)) return dF; //SEROSA SOLLBRUCHSTELLE

    float alpha = 0.000085;
    float r_target = 0.01;

    if (i == j) {
        dF.r=alpha*(r_target-Xi.r);
        dF += d_W[i];

        return dF;
    }

    float rc = Xi.r + (Xi.r - r.r);
    if (dist > rc*1.5) return dF;

    d_num_neighs[i]++;

    // r = Xi - Xj | r - Xi = - Xj | Xi - r = Xj

    float a= 3.0;
    auto F = fmaxf(rc - dist, 0) * 2 - fmaxf(dist - rc, 0)*a;

    d_forces_mechanical[i] += F;

    dF.x = r.x * F / dist;
    dF.y = r.y * F / dist;
    dF.z = r.z * F / dist;

    return dF;
}

__global__ void generate_noise(int n, curandState* d_state) {
    auto i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= n) return;

    float D = 0.0;

    d_W[i].x = curand_normal(&d_state[i]) * powf(dt, 0.5) * D / dt;
    d_W[i].y = curand_normal(&d_state[i]) * powf(dt, 0.5) * D / dt;
    d_W[i].z = curand_normal(&d_state[i]) * powf(dt, 0.5) * D / dt;
    d_W[i].r = 0.0;
}

__global__ void kernel_force_to_surface(int n, int n_surface, const Cell* __restrict__ d_X, Cell* d_dX) {
    auto i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= n) return;

    int minID = 0;
    float3 Xi{0};
    Xi.x = d_X[i].x; Xi.y = d_X[i].y; Xi.z = d_X[i].z;

    float3 r = Xi - d_surface[0];

    float minD = norm3df(r.x, r.y, r.z);

    for (int j = 1; j < n_surface; j++) {
        r = Xi - d_surface[j];
        float D = norm3df(r.x, r.y, r.z);
        if (D<minD) {
            minID = j;
            minD = D;
        }
    }

    r = Xi - d_surface[minID];
    float k = 10.0;
    float F = - k * (r.x * d_normals[minID].x + r.y * d_normals[minID].y + r.z * d_normals[minID].z);

    d_forces_surface[i] = F;

    float3 dF = F * d_normals[minID];
    d_dX[i].x += dF.x; d_dX[i].y += dF.y; d_dX[i].z += dF.z;
    return;

}

void generic(int n, const Cell* __restrict__ d_X, Cell* d_dX, int n_surface) {
    kernel_force_to_surface<<<(n_cells + 32 - 1)/32, 32>>>(n, n_surface, d_X, d_dX);
}

int main(int argc, char *argv[]) {
    ///for (int REPETITION=1; REPETITION<=1; REPETITION++) {

    /*
    Prepare Random Variable for the Implementation of the Wiener Process
    */
    curandState* d_state;
    cudaMalloc(&d_state, n_cells*sizeof(curandState));
    auto seed = time(NULL);
    setup_rand_states<<<(n_cells + 32 - 1)/32, 32>>>(n_cells, seed, d_state);

    Property<Cell> W{n_cells, "wiener_process"};
    cudaMemcpyToSymbol(d_W, &W.d_prop, sizeof(d_W));

    /*
    Prepare the Surface on Which the Cells Shall Move
    */
    Vtk_input input_surface{"./surface_D.vtk"};
    int n_surface = input_surface.n_points;
    Solution<float3, Tile_solver> surface{n_surface};
    input_surface.read_positions(surface);
    for (int i = 0; i < n_surface; i++) {
        //Rechteck (surface_C, normals_C)
        //surface.h_X[i] *= 6.5;

        //Kugel (surface_B, normals_B)
        //surface.h_X[i] *= 4.7;

        //Ellipsoid (surface_E, normals_E)
        //surface.h_X[i] *= 0.85;

        //Tribolium Castaneum (surface_D, normals_D)
        surface.h_X[i] *= 0.305;
    }
    Vtk_input input_normals{"./normals_D.vtk"};
    //normals_B
    //normals_ellipse3
    //normals_D
    Solution<float3, Tile_solver> normals{n_surface};
    input_normals.read_positions(normals);

    surface.copy_to_device();
    normals.copy_to_device();

    cudaMemcpyToSymbol(d_surface, &surface.d_X, sizeof(d_surface));
    cudaMemcpyToSymbol(d_normals, &normals.d_X, sizeof(d_normals));

    /*
    Generate the Cells
    */
    Solution<Cell, Gabriel_solver> cells{n_cells, 100, r_max};
    //std::cout<<"./1sphere/sphere"+std::to_string(int(REPETITION))+".vtk\n";
    Vtk_input input_cells{"./start_confi.vtk"};//+std::to_string(int(REPETITION))+".vtk"}; //input_ellipsoid.vtk, input_serosa.vtk
    input_cells.read_positions(cells);
    //random_sphere(r_max, cells);

    Property<int> num_neighs{n_cells, "num_neighs"};
    Property<float> forces_mechanical{n_cells, "forces_mechanical"};
    Property<float> forces_surface{n_cells, "forces_surface"};

    for (int i = 0; i < n_cells; i++) {
        num_neighs.h_prop[i] = 0;
        forces_mechanical.h_prop[i] = 0;
        forces_surface.h_prop[i] = 0;

        cells.h_X[i].z += 0.0;
        cells.h_X[i].r = 0.35;
    }
    num_neighs.copy_to_device();
    forces_mechanical.copy_to_device();
    forces_surface.copy_to_device();
    cells.copy_to_device();

    cudaMemcpyToSymbol(d_num_neighs, &num_neighs.d_prop, sizeof(d_num_neighs));
    cudaMemcpyToSymbol(d_forces_mechanical, &forces_mechanical.d_prop, sizeof(d_forces_mechanical));
    cudaMemcpyToSymbol(d_forces_surface, &forces_surface.d_prop, sizeof(d_forces_surface));

    /*
    Define the Generic Forces
    */

    auto fun = [&](const int n, const Cell* __restrict__ d_X, Cell* d_dX) {
        thrust::fill(thrust::device, num_neighs.d_prop, num_neighs.d_prop + n_cells, 0);
        thrust::fill(thrust::device, forces_mechanical.d_prop, forces_mechanical.d_prop + n_cells, 0);
        generic(n, d_X, d_dX, n_surface);
    };

    /*
    Output File
    */
    //Vtk_output output{"example"+std::to_string(int(REPETITION))};
    Vtk_output output{"outcome"};
    //1serosa*/serosa*{nr}.vtk
    for (int t = 0; t < tMax; t++) {
        cells.copy_to_host();
        num_neighs.copy_to_host();
        forces_mechanical.copy_to_host();
        forces_surface.copy_to_host();

        for (float T = 0.0; T < 2.0; T+=dt) {
            generate_noise<<<(n_cells + 32 - 1)/32, 32>>>(n_cells, d_state);
            cells.take_step<force_function, friction_on_background>(dt, fun);
        }

        output.write_positions(cells);
        output.write_field(cells, "radius", &Cell::r);  // For visualization
        output.write_property(num_neighs);
        output.write_property(forces_mechanical);
        output.write_property(forces_surface);
    }

    /*
    cells.copy_to_host();
    num_neighs.copy_to_host();
    forces_mechanical.copy_to_host();
    forces_surface.copy_to_host();

    output.write_positions(cells);
    output.write_field(cells, "radius", &Cell::r);  // For visualization
    output.write_property(num_neighs);
    output.write_property(forces_mechanical);
    output.write_property(forces_surface);
    */

    cudaFree(d_state);
    //}
    return 0;
}
