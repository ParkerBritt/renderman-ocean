#!/usr/bin/env bash

./build.sh "$@"
cd ./build
prman out_*.rib
