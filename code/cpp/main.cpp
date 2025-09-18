#include "solver.h"

using namespace std;

Float3 f(Float3 vi, Float3 vj) {
    double a = 0.6;
    double r_c = 0.5;
    double sig = 2;
    Float3 tempV = vj - vi;
    double d = tempV.leng();
    Float3 dir = tempV / d;
    if (d > sig*r_c) return Float3(0, 0, 0);
    double F = 2 * ( exp(-2*a*(d - r_c)) - exp(-a*(d - r_c))); 
    return (dir * F); 
}

int main() {
    Scene scene = Scene(10000, 1000, 0.1);
    runSimulation(scene, 0.4, 40.8, "test", f, "output");
}
