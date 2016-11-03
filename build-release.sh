#!/bin/bash
# This script sets up build requirements to generate an executable with pyinstaller
mkdir release-linux
cd release-linux
pyinstaller --onefile --windowed --icon=../installer/resource/install.ico ../installer/installer.py
cp ./dist/installer ./
cp -rf ../installer/resource ./
cp ../DSPH.py ./resource/
cp ../LICENSE ./resource/
cp -rf ../DSPH_Images/ ./resource/
rm ./installer.spec
rm -rf ./build
rm -rf ./dist
