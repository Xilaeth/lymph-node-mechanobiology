#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <sstream>
#include <cmath>

using namespace std;

vector<vector<double>> loadVtk(string file) {
    ifstream inp(file);

    string line;
    vector<string> content;
    while(getline(inp, line)) {
        content.push_back(line);
    }
    content.erase(content.begin(), content.begin() + 6);

    vector<vector<double>> output;

    for (auto& l : content) {
        vector<string> coords; 
        stringstream ss(l);
        string temp;
        while(ss >> temp) {
            coords.push_back(temp);
        }
        output.push_back({stod(coords[0]), stod(coords[1]), stod(coords[2])});
    }
    return output;
}

bool isInCirc(vector<double> v, vector<double> x, double r) {
    if ((pow(v[0] - x[0], 2) + pow(v[1] - x[1], 2)) < r*r) {
        return true;
    }
    return false;
}

double densityInCirc(vector<double> x, double r, vector<vector<double>>& inp) {
    unsigned int counter = 0;
    for (auto& v : inp) {
        if (isInCirc(v, x, r)) counter++;
    }
    return (double)(counter/(M_PI*r*r));
}

int main() {
    vector<vector<double>> inp = loadVtk("lines_out.vtk");

    double l = 15; 
    unsigned int n = 100;
    double r = 2;
    double x = 10;
    double y = 7;
    string loc = "lines_out_data";

    string endup = "";
    endup.append(loc);
    endup.append(".csv");
    ofstream temp_file (endup);

    for (int i = 0; i <= n; i++) {
        for (int j = 0; j <= n; j++) {
            temp_file << i << "," << j << "," << densityInCirc({-l/2 + x + i*(l/n), -l/2 + y + j*(l/n)}, r, inp) << endl;
        }
    }
}
