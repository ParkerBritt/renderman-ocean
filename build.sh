#!/usr/bin/env bash

# make build dir
mkdir -p build/bin

rm build/out_*.rib

# shaders
cp -ur ./src/scene/textures ./build/
oslc src/scene/shaders/water.osl -o build/water.oso

# scene
cd src/scene
./build_rib.py "$@"

