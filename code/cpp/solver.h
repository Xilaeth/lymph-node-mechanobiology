#ifndef SOLVER_H
#define SOLVER_H

#include <cmath>

class Float3 {
    public:
        double x;
        double y;
        double z;

        Float3(double x_, double y_, double z_) : x{x_}, y{y_}, z{z_} {}

        Float3 operator*(double a) {
            return Float3(a * x, a*y, a*z);
        }

        double operator*(Float3 v2) {
            return (x*v2.x + y*v2.y + z*v2.z);
        }
  
        Float3 operator/(double a) {
            return Float3(x/a, y/a, z/a);
        }
};

class Cell {
    public:
        Cell(
};


#endif
