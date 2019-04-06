#!/bin/sh

# Install Minisat solver binary dependency used by satispy, assuming Ubuntu
sudo apt -y install minisat
# Install satispy
pip3 install --user satispy numpy
