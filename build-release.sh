#!/bin/bash
# This script sets up build requirements to generate an executable with pyinstaller
mkdir release-linux
cd release-linux
pyinstaller --onefile --windowed --icon=../installer/resource/install.ico ../installer/installer.py
cp ./dist/installer ./
cp -rf ../installer/resource ./
cp ../DesignSPHysics.py ./resource/
cp ../DesignSPHysics.FCMacro ./resource/
cp ../default-config.json ./resource/
cp ../LICENSE ./resource/
cp -rf ../images/ ./resource/
cp -rf ../mod/ ./resource/
cp -rf ../dualsphysics/ ./resource/
rm ./installer.spec
rm -rf ./build
rm -rf ./dist
chmod -R 777 .
cd ..
tar -zcvf release-linux.tar.gz release-linux/
rm -r release-linux/