#include "solver.h"

using namespace std;

int main() {
    Float3 v = Float3(1, 2, 3);

    Scene scene = Scene(100, 0.01, 1000);
    scene.loadRectangle(1.0, 5.0);

    K3Tree k = K3Tree(scene);
}
