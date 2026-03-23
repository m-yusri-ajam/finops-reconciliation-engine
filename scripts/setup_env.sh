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

# 3. Install Python Libraries (User-level to prevent OS conflicts)
# Note: We use --upgrade to ensure we have the latest stable versions.
echo "Installing Data Science & Web Stack..."
pip3 install --user --upgrade \
    pandas \
    numpy \
    scikit-learn \
    flask \
    sqlalchemy \
    requests

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
