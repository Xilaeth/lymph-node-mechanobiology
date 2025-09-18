#include <cmath>
#include <vector>
#include <iostream>
#include <fstream>
#include <string>
#include <memory>
#include <algorithm>
#include <queue>
#include <random>
#include <iomanip>
#include <sstream>

using namespace std;

// simple 3-vector class
class Float3 {
    public:
        double x;
        double y;
        double z;
        unsigned int ind;

        vector<unsigned int> neighbors;

        Float3(double x_, double y_, double z_, unsigned int ind_ = 0) : x{x_}, y{y_}, z{z_}, ind{ind_} {}

        Float3 operator*(double a) {
            return Float3(a * x, a*y, a*z, ind);
        }

        Float3 operator+(Float3 v) {
            return Float3(v.x + x, v.y + y, v.z + z, ind);
        }

        Float3 operator-(Float3 v) {
            return Float3(v.x - x, v.y - y, v.z - z, ind);
        }

        double operator*(Float3& v2) {
            return (x*v2.x + y*v2.y + z*v2.z, ind);
        }
  
        Float3 operator/(double a) {
            return Float3(x/a, y/a, z/a, ind);
        }

        double leng() {
            return sqrt(x*x + y*y + z*z);
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
        double totForce;

        Scene(unsigned int n_cells, unsigned int steps, double dt): n_cells{n_cells}, steps{steps}, dt{dt} {}

        // starts the scene with cells arranged in a rectangle with x length lx and a distance to the nearest cells of d
        void loadRectangle(double d, double lx) {
            double x = -lx/2 + d;
            double y = -lx/2 + d;
            for (int i = 0; i < n_cells; i++) {
                x += d;
                if ((x + d) >= lx/2) {
                    x = -lx/2 + d;
                    y += d;
                }
                cells.push_back(Float3(x, y, 0, i));
            }
        }

        // load a simulation from a vtk file
        void loadVtk(string file) {
            ifstream inp(file);

            string line;
            vector<string> content;
            while(getline(inp, line)) {
                content.push_back(line);
            }
            n_cells = content.size() - 6;
            content.erase(content.begin(), content.begin() + 6);

            unsigned int index = 0;

            for (auto& l : content) {
                vector<string> coords; 
                stringstream ss(l);
                string temp;
                while(ss >> temp) {
                    coords.push_back(temp);
                }
                cells.push_back(Float3(stod(coords[0]), stod(coords[1]), stod(coords[2]), index));
                index++;
            }
        }

        // updates neighbors to conform with a gabriel graph
        // maybe switch the neighbor vector to contain Float3s but it works for now
        void updateGabriel() {
            for (auto& c : cells) {
                vector<unsigned int> tempV;
                for (auto i : c.neighbors) {
                    bool add = true;
                    Float3 q = (c + cells[i])/2.f;
                    double r = (c - cells[i]).leng() / 2.f;
                    for (auto j : c.neighbors) {
                        if (i == j) continue; 
                        double d = (q - cells[j]).leng();
                        if (d < r) add = false;
                    }
                    if (add) tempV.push_back(i);
                }
                c.neighbors = tempV;
            }
        }

        // takes a time step in the scene
        // for the time being without stochasticity
        void takeStep(Float3 (*force)(Float3, Float3)) {
            totForce = 0;
            double b = 0.1*sqrt(dt);
            random_device rd;
            mt19937 gen(rd());

            normal_distribution<> dist(0.0, 1.0);

            for (auto& c : cells) {
                Float3 tempF = Float3(0, 0, 0); 
                for (auto i : c.neighbors) {
                    tempF = tempF + force(c, cells[i]);
                }
                 
                totForce += tempF.leng(); 
                c.x += tempF.x * dt + b*dist(gen);
                c.y += tempF.y * dt + b*dist(gen);
                c.z += tempF.z * dt; // + b*dist(gen);
            }
            cout << totForce << ",";
        }

        
        // saves current scence to the provided string
        void saveScene(string loc, string folder) {
            string endup = "";
            endup.append(folder);
            endup.append(loc);
            endup.append(".vtk");
            ofstream temp_file (endup);
            temp_file << "# vtk DataFile Version 3.0" << endl;
            temp_file << loc << endl;
            temp_file << "ASCII" << endl;
            temp_file << "DATASET POLYDATA" << endl;
            temp_file << endl;
            temp_file << "POINTS " << n_cells << " float" << endl;
            for (auto c : cells) {
                temp_file << setprecision(5) << c.x << " " << c.y << " " << c.z << "\n";
            }
            temp_file.close();
        }
};

// k-d-tree for 3 dimensions (ChatGPT was used to construct this class. Nothing was straight up copied due to me having to make it compatible with my previously defined classes. Still information for transparency)
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

        auto comparator = [axis](const Float3 &a, const Float3 &b) {
            if (axis == 0) return a.x < b.x;
            else if (axis == 1) return a.y < b.y;
            else return a.z < b.z;
        };

        // sorts the points so that the mid point is in the correct place, the smaller ones beneath and the bigger ones on top
        nth_element(points.begin() + start, points.begin() + mid, points.begin() + end, comparator);

        auto node = make_unique<Node>(points[mid], axis);
        node->left = build(points, depth + 1, start, mid);
        node->right = build(points, depth + 1, mid+1, end);

        return node;
    }

    static double squaredDistance(const Float3& a, const Float3& b) {
        return (a.x - b.x) * (a.x - b.x) +
               (a.y - b.y) * (a.y - b.y) +
               (a.z - b.z) * (a.z - b.z);
    }

    void nearest(Node* node, Float3& target, Float3& best, double& bestDist) const {
        if (!node) return;

        double dist = squaredDistance(node->point, target);
        if (dist < bestDist) {
            bestDist = dist;
            best = node->point;
        }

        double diff = (target.getCoord())[node->axis] - ((node->point).getCoord())[node->axis];
        Node* first = diff < 0 ? node->left.get() : node->right.get();
        Node* second = diff < 0 ? node->right.get() : node->left.get();

        nearest(first, target, best, bestDist);

        if (diff * diff < bestDist) {
            nearest(second, target, best, bestDist);
        }
    }

    template <typename Queue>
    void kNearest(Node* node, Float3& target, int k, Queue& heap) {
        if (!node) return;

        double dist = squaredDistance(node->point, target);

        if ((int)heap.size() < k) {
            heap.push({dist, node->point});
        } else if (dist < heap.top().first) {
            heap.pop();
            heap.push({dist, node->point});
        }

        double diff = (target.getCoord())[node->axis] - ((node->point).getCoord())[node->axis];
        Node* first = diff < 0 ? node->left.get() : node->right.get();
        Node* second = diff < 0 ? node->right.get() : node->left.get();

        kNearest(first, target, k, heap);

        if ((int)heap.size() < k || diff * diff < heap.top().first) {
            kNearest(second, target, k, heap);
        }
    }

    public:

        K3Tree(vector<Float3> cells) {
            root = build(cells, 0, 0, cells.size());
        }
        
        double nearestNeighbor(Float3& target, Float3& best) const {
            double bestDist = std::numeric_limits<double>::max();
            nearest(root.get(), target, best, bestDist);
            return bestDist;
        }

        std::vector<std::pair<Float3, double>> kNearestNeighbors(Float3& target, int k) {
            auto cmp = [](std::pair<double, Float3>& a, std::pair<double, Float3>& b) {
                return a.first < b.first; // max-heap by distance
            };
            std::priority_queue<std::pair<double, Float3>,std::vector<std::pair<double, Float3>>,decltype(cmp)> heap(cmp);

            kNearest(root.get(), target, k, heap);

            std::vector<std::pair<Float3, double>> result;
            while (!heap.empty()) {
                result.push_back({heap.top().second, heap.top().first});
                heap.pop();
            }
            std::reverse(result.begin(), result.end()); // closest first
            return result;
        }

        void setNeighbors(Scene& scene) {
            K3Tree temp = K3Tree(scene.cells); 
            int numNeigh = 8;
            for (auto& c : scene.cells) {
                auto tempRes = temp.kNearestNeighbors(c, numNeigh);
                vector<unsigned int> tempV;
                for (auto& [pt, k] : tempRes) {
                    if (pt.ind == c.ind) continue;
                    tempV.push_back(pt.ind);
                }
                c.neighbors = tempV;
            }
        }
};

void runSimulation(Scene& scene, double d, double lx, string prefix, Float3 (*force)(Float3, Float3), string folder = "") {
    scene.loadRectangle(d, lx);
    //scene.loadVtk("hole_out.vtk");
    if (folder != "") folder.append("/");

    unsigned int j = 0;
    for (unsigned int i = 0; i <= scene.steps; i++) {
        string save = "";
        save.append(prefix);
        save.append(to_string(j));
        if (i == 0) {scene.saveScene(save, folder); j++; continue;}
        K3Tree tree = K3Tree(scene.cells);  
        tree.setNeighbors(scene);
        scene.updateGabriel();
        scene.takeStep(force);
        if ((i % 10) == 0) {j++; scene.saveScene(save, folder);}
        //if(i == scene.steps) scene.saveScene(save, folder);
    }
}
