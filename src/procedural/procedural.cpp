#include <iostream>
#include <vector>
#include <sstream>
#include <cmath>

class Point {
public:
    float x;
    float y;
    float z;

    Point(float _x, float _y, float _z){
        x = _x;
        y = _y;
        z = _z;
    }
};

int main(){
    std::ios::sync_with_stdio(false);
    std::ostringstream outputBuffer;
    // std::vector<std::vector<float>> grid = {
    //     {0.1, 0.0, 0.2, 0.1, 0.0, -0.1, -0.2, 0.0, 0.1, -0.2, 0.0, -0.1},
    //     {0.2, 0.0, 0.1, 0.2, 0.0, -0.2, 0.0, 0.0, 0.2, 0.0, 0.0, -0.1},
    //     {1.0, 1.0, 0.5, 1.0, 1.0, -0.5, 0.0, 0.0, 0.5, 0.0, 0.0, -0.5},
    //     {0.5, 0.0, 0.5, 0.5, 0.0, -0.5, -0.5, 0.0, 0.5, -0.5, 0.0, -0.5},
    //     {1.0, 1.0, 0.5, 1.0, 1.0, -0.5, 0.0, 0.0, 0.5, 0.0, 0.0, -0.5},
    //     {0.1, 0.0, 0.2, 0.1, 0.0, -0.1, -0.2, 0.0, 0.1, -0.2, 0.0, -0.1},
    //     {0.5, 0.0, 0.5, 0.5, 0.0, -0.5, -0.5, 0.0, 0.5, -0.5, 0.0, -0.5},
    //     {0.2, 0.0, 0.1, 0.2, 0.0, -0.2, 0.0, 0.0, 0.2, 0.0, 0.0, -0.1},
    //     {0.5, 0.0, 0.5, 0.5, 0.0, -0.5, -0.5, 0.0, 0.5, -0.5, 0.0, -0.5},
    //     {1.0, 1.0, 0.5, 1.0, 1.0, -0.5, 0.0, 0.0, 0.5, 0.0, 0.0, -0.5},
    //     {0.5, 0.0, 0.5, 0.5, 0.0, -0.5, -0.5, 0.0, 0.5, -0.5, 0.0, -0.5},
    //     {1.0, 1.0, 0.5, 1.0, 1.0, -0.5, 0.0, 0.0, 0.5, 0.0, 0.0, -0.5},
    // };

    std::vector<std::vector<float>> grid(100, std::vector<float>(100, 0.0f));

    if(grid.size() % 2 != 0 || grid[0].size() % 2 != 0  || grid.size()<2 || grid[0].size()<2){
        throw std::length_error("Grid must be >= 2x2 and even (for now)");
    }
    const float GRID_SCALE=0.5;
    const float HEIGHT_SCALE=0.1;
    float grid_start_x = 0;
    float grid_start_z = 0.25f*grid.size()-GRID_SCALE/2; // ofset grid edge to z
    // center grid
    grid_start_x += -GRID_SCALE/2 * (grid[0].size()-1) + GRID_SCALE/2;
    grid_start_z += GRID_SCALE/2 * (grid.size()-1) - GRID_SCALE/2;

    for(size_t row=0; row<grid.size()-1; row++){
        for(size_t col=0; col<grid[row].size()-1; col++){
            grid[row][col] = std::sin((row+col)/2)*2;

        }
    }

    for(size_t row=0; row<grid.size()-1; row++){
        for(size_t col=0; col<grid[row].size()-1; col++){
            // std::cout << "# row: " << row << '\n';
            // std::cout << "# col: " << col << '\n';
            // continue;
            outputBuffer << "Patch \"bilinear\" \"P\" ["
            << grid_start_x + 0.5*GRID_SCALE + (GRID_SCALE * col) << ' '   // x1
            << grid[row][col+1] * HEIGHT_SCALE << ' '   // y1
            << grid_start_z + 0.5*GRID_SCALE - (GRID_SCALE * row) << ' '   // z1
            << grid_start_x + 0.5*GRID_SCALE + (GRID_SCALE * col) << ' '   // x2
            << grid[row+1][col+1] * HEIGHT_SCALE << ' '   // y2
            << grid_start_z + -0.5*GRID_SCALE - (GRID_SCALE * row) << ' '  // z2
            << grid_start_x + -0.5*GRID_SCALE + (GRID_SCALE * col) << ' '  // x3
            << grid[row][col] * HEIGHT_SCALE << ' '   // y3
            << grid_start_z + 0.5*GRID_SCALE - (GRID_SCALE * row) << ' '   // z3
            << grid_start_x + -0.5*GRID_SCALE + (GRID_SCALE * col) << ' '  // x4
            << grid[row+1][col] * HEIGHT_SCALE << ' '   // y4
            << grid_start_z + -0.5*GRID_SCALE - (GRID_SCALE * row)         // z4
            <<"]\n";

            // if(i%12==0){
                // if(i>0) std::cout <<"]\n";
            // }
            // float component = grid[0][i];
            // std::cout << component << ' ';
        }
    }
    std::cout << outputBuffer.str();
    std::cout << '\377';
}
