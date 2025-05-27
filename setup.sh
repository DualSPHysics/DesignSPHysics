#!/bin/bash

# Ensure the target directory exists
mkdir -p dualsphysics

# Download the contents of CCC/BBB into AAA/BBB
wget -r -np -nH --cut-dirs=2 -P . \
     --accept "*.linux64,*.exe,*.so,*.dll,*.out,*.txt,*.zip,*.tar,*.gz" \
     --reject "*.html*,*index*" \
     "https://dual.sphysics.org/sphcourse/DualSPHysics-bin/dualsphysics.tar.gz"

tar -xf dualsphysics.tar.gz
rm -rf dualsphysics.tar.gz

chmod +x dualsphysics/bin/*

echo "Download completed"
