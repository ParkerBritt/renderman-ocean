#!/usr/bin/env bash

mkdir -p build/bin

# shaders
cp -ur ./src/scene/textures ./build/
oslc src/scene/shaders/water.osl -o build/water.oso

# scene
cd src/procedural
g++ -g procedural.cpp -o ../../build/bin/procedural
cd ../scene
./build_rib.py

