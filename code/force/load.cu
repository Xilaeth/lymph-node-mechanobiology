// Integrate N-body problem with springs between all bodies
#include "../include/dtypes.cuh"
#include "../include/inits.cuh"
#include "../include/solvers.cuh"
#include "../include/vtk.cuh"
#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <sstream>
#include <cmath>

const auto r_c = 0.5f; // equilibrium distance
__device__ double dt = 0.05f; // time step
__device__ int n_time_steps = 50u;
//__device__ int n_cells = 1000;
__device__ double a = 1.0f;
__device__ double r_max = 1.0f;

MAKE_PT(Cell, f);
    
using namespace std;

__device__ Cell morse(Cell Xi, Cell r, float dist, int i, int j)
{
    Cell dF{0}; // 0 vector
    if (i == j) return dF; // if the two indeces are the same return the 0-vector
    if (dist > r_max) return dF; // if the distance is greater than the maximum interaction length it's also the 0 vector

    float F = 2 * (exp(-2*a*(dist - r_c)) - exp(-a*(dist - r_c))); // strength of the Morse potential

    dF.x = r.x * F / dist;
    dF.y = r.y * F / dist;
    dF.z = r.z * F / dist;
    dF.f = F;

    return dF; // return force that's to be applied
}

// order of parameters is: n_cells, 
int main(int argc, const char* argv[])
{
    a = stod(argv[1]); // repulsion strength of the morse potential
    r_max = r_c * stod(argv[2]); // maximum interaction length
    string file = argv[3]; // input file name
    n_time_steps = stoi(argv[4]);
    dt = stod(argv[5]);
    int every_n = stoi(argv[6]);

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
    cells.copy_to_device();

    // Integrate positions
    Vtk_output output{"out"};  // Writes to output/relax_#.vtk
    for (auto time_step = 0; time_step <= n_time_steps; time_step++) {
        cells.copy_to_host();
        cells.take_step<morse>(dt);    // Ordered to write during calculation,
        if ((time_step % every_n) == 0) {
            output.write_positions(cells);  // use thread for full concurrency.
            output.write_field(cells, "f", &Cell::f);
        }
    }

    return 0;
}
