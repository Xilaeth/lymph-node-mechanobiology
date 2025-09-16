#include <cmath>
#include <vector>
#include <iostream>
#include <fstream>
#include <string>
#include <memory>
#include <algorithm>

using namespace std;

// simple 3-vector class
class Float3 {
    public:
        double x;
        double y;
        double z;

        Float3(double x_, double y_, double z_) : x{x_}, y{y_}, z{z_} {}

        Float3 operator*(double a) {
            return Float3(a * x, a*y, a*z);
        }

        double operator*(Float3& v2) {
            return (x*v2.x + y*v2.y + z*v2.z);
        }
  
        Float3 operator/(double a) {
            return Float3(x/a, y/a, z/a);
        }

        vector<double> getCoord() {
            return {x, y, z};
        }
};

// class that represents the state of the system
class Scene {
    public:
        unsigned int n_cells;
        double dt;
        unsigned int steps;

        vector<Float3> cells;

        Scene(unsigned int n_cells, unsigned int steps, double dt): n_cells{n_cells}, steps{steps}, dt{dt} {}

        // starts the scene with cells arranged in a rectangle with x length lx and a distance to the nearest cells of d
        void loadRectangle(double d, double lx) {
            double x = 0;
            double y = 0;
            for (int i = 0; i < n_cells; i++) {
                if ((x + d) >= lx) {
                    x = d;
                    y += d;
                }
                x += d;
                cells.push_back(Float3(x, y, 0));
            }
        }
        
        // saves current scence to the provided string
        void saveScene(string loc) {
            ofstream temp_file (loc);
            for (auto c : cells) {
                temp_file << c.x << " " << c.y << " " << c.z << "\n";
            }
            temp_file.close();
        }
};

// k-d-tree for 3 dimensions
class K3Tree {
    private:
        // node struct
        struct Node {
            Float3 point;
            unique_ptr<Node> left;
            unique_ptr<Node> right;
            int axis; // 0 = x; 1 = y; 2 = z
            
            Node(const Float3& pt, int ax) : point(pt), axis(ax) {}
        };

    unique_ptr<Node> root;

    // recursively builds the k-d-tree
    unique_ptr<Node> build(vector<Float3>& points, int depth, int start, int end) {
        if (start >= end) return nullptr;

        int axis = depth % 3;
        int mid = (start + end) / 2;

        // sorts the points so that the mid point is in the correct place, the smaller ones beneath and the bigger ones on top
        nth_element(points.begin() + start, points.begin() + mid, points.begin() + end, [axis](Float3& a, Float3& b) {return (a.getCoord())[axis] < (b.getCoord())[axis];});

        auto node = make_unique<Node>(points[mid], axis);
        node->left = build(points, depth + 1, start, mid);
        node->right = build(points, depth + 1, mid, end);

        return node;
    }

    public:

        K3Tree(Scene scene) {
            vector<Float3> pts = scene.cells;
            root = build(pts, 0, 0, pts.size());
        }
};
