#include <iostream>
#include <vector>

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
    std::vector<std::vector<float>> grid = {{
        0.5, 0.0, 0.5, 0.5, 0.0, -0.5, -0.5, 0.0, 0.5, -0.5, 0.0, -0.5,
        1.0, 1.0, 0.5, 1.0, 1.0, -0.5, 0.0, 0.0, 0.5, 0.0, 0.0, -0.5
    }};
    for(size_t i=0; i<grid[0].size(); i++){
        if(i%12==0){
            if(i>0) std::cout <<"]\n";
            std::cout << "Patch \"bilinear\" \"P\" [";
        }
        float component = grid[0][i];
        std::cout << component << ' ';
    }
    std::cout <<"]\n";
    std::cout << '\377';
}
