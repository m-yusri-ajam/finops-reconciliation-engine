#!/bin/bash

# =================================================================
# Project: Financial Data Automation Environment Setup
# Author: Yusri Ajam
# Description: Provisions an Ubuntu environment with the 
#              necessary Python stack and VS Code for FinOps.
# =================================================================

# 1. Update System Packages
echo "Checking for system updates..."
sudo apt update && sudo apt upgrade -y

# 2. Install Python3 and Pip if not present
echo "Installing Python3 and Pip..."
sudo apt install -y python3 python3-pip

# 3. Setup Virtual Environment at Project Root
echo "Determining Project Root..."

# Get the absolute path of the directory where the script is located
SCRIPT_PATH=$(readlink -f "$0")
SCRIPT_DIR=$(dirname "$SCRIPT_DIR") # This is 'scripts'
ROOT_DIR=$(dirname "$SCRIPT_DIR")   # This is the 'root'

cd "$ROOT_DIR"
echo "Root directory identified as: $ROOT_DIR"

# Create the environment
python3 -m venv .venv

# Use the absolute path to the new pip to install libraries
echo "Installing Data Science & Web Stack into $ROOT_DIR/.venv..."
"$ROOT_DIR/.venv/bin/pip" install --upgrade \
    pandas \
    numpy \
    scikit-learn \
    flask \
    sqlalchemy \
    requests \
    thefuzz \
    python-Levenshtein

# 4. Install VS Code via Snap (Standard for Ubuntu)
if ! command -v code &> /dev/null; then
    echo "Installing VS Code..."
    sudo snap install --classic code
else
    echo "VS Code is already installed."
fi

echo "----------------------------------------------------"
echo "Setup Complete! Environment is ready for FinOps."
echo "----------------------------------------------------"
