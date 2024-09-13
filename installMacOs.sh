#!/bin/bash

# Update Homebrew
brew update

# Install solc
brew tap ethereum/ethereum
brew install solc

# Install solc-select
brew install solc-select

# Install Slither
pip3 install slither-analyzer

# Install cspell
npm install -g cspell

# Install Mythril
pip3 install mythril

echo "All tools have been installed successfully on macOS!"