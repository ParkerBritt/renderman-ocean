#!/usr/bin/env bash

mkdir -p build/bin
cd src/procedural
g++ procedural.cpp -o ../../build/bin/procedural
cd ../scene
./build_rib.py
