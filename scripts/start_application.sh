#!/bin/bash
cd /home/ec2-user/banking_crud
export DB_HOST="banking-db-tht.ctgu00g8ckle.ap-southeast-1.rds.amazonaws.com"
export DB_NAME="bankingdb"
export DB_USER="thtadmin"
export DB_PASSWORD=$(aws secretsmanager get-secret-value --secret-id crud-application-secrets --query SecretString --output text | jq -r '.DB_PASSWORD')

# Stop any existing service
pkill -f gunicorn || true

# Start Flask app using Gunicorn
gunicorn --bind 0.0.0.0:5000 banking_crud:app --daemon
