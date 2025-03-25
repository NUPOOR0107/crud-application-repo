#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

echo "Installing dependencies..."
mkdir -p /home/ec2-user/banking_crud
cd /home/ec2-user/banking_crud

python --version
python3 --version

# Install Pip
curl -O https://bootstrap.pypa.io/get-pip.py
# python3 get-pip.py

# Install Python dependencies
pip3 install --no-cache-dir -r requirements.txt

echo "Dependencies installed successfully."
