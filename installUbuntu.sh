#!/bin/bash

# Update package list
sudo apt-get update

# Install solc
sudo apt-get install -y solc

# Install solc-select
pip3 install solc-select

# Install Slither
pip3 install slither-analyzer

# Install cspell
npm install -g cspell

echo "All tools have been installed successfully on Ubuntu!"