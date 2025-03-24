#!/bin/bash
set -e  # Exit script on any error

echo "Updating system packages..."
sudo yum update -y

echo "Installing Python and pip..."
sudo yum install -y python3 python3-pip

echo "Installing required dependencies..."
pip3 install --upgrade pip
pip3 install -r /home/ec2-user/banking_crud/requirements.txt

echo "Installing AWS CodeDeploy Agent..."
sudo yum install -y ruby wget
cd /home/ec2-user
wget https://github.com/aws/aws-codedeploy-agent/releases/latest/download/codedeploy-agent.noarch.rpm
sudo yum install -y codedeploy-agent.noarch.rpm
sudo systemctl start codedeploy-agent
sudo systemctl enable codedeploy-agent

echo "Installation completed successfully!"
