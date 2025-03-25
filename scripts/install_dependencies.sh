#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

echo "Installing dependencies..."

# Navigate to the deployment directory
cd /home/ec2-user/banking_crud

# Unzip the application package
echo "Extracting banking_crud.zip...."
unzip -o banking_crud.zip
rm -f banking_crud.zip  # Remove the ZIP file after extraction

# Check Python version
python3 --version

# Install Pip if not already installed
if ! command -v pip3 &> /dev/null; then
    echo "Installing Pip..."
    curl -O https://bootstrap.pypa.io/get-pip.py
    python3 get-pip.py
fi

# Install Python dependencies
pip3 install --no-cache-dir -r requirements.txt

echo "Dependencies installed successfully."
