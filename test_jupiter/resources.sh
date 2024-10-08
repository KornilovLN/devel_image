#!/bin/bash
echo " "
echo "=== Python Version ==================================="
python --version

echo " "
echo "=== R Version ========================================"
R --version

echo " "
echo "=== Julia Version ===================================="
julia --version

echo " "
echo "=== Python Libraries ================================="
pip list

echo " "
echo "=== R Packages ======================================="
R -e 'installed.packages()'

echo " "
echo "=== Julia Packages ==================================="
julia -e 'using Pkg; Pkg.status()'

echo " "
echo "=== System Packages =================================="
dpkg --list
