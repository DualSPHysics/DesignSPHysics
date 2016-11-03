#!/bin/bash
# This script sets up build requirements to generate an executable with pyinstaller
mkdir release-linux
cd release-linux
pyinstaller --onefile --windowed --icon=../installer/resource/install.ico ../installer/installer.py
cp ./dist/installer ./
cp ../DSPH.py ./
cp ../LICENSE ./
cp -rf ../DSPH_Images/ ./
cp -rf ../installer/resource ./
rm ./installer.spec
rm -rf ./build
rm -rf ./dist
