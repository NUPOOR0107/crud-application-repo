#!/bin/bash
set -e  # Exit if any command fails

echo "Starting Flask application..."

cd /home/ec2-user/banking_crud

# Load environment variables from AWS Secrets Manager
export DB_HOST="banking-db-tht.ctgu00g8ckle.ap-southeast-1.rds.amazonaws.com"
export DB_NAME="bankingdb"
export DB_USER="thtadmin"

# Fetch DB password securely
DB_PASSWORD_JSON=$(aws secretsmanager get-secret-value --secret-id crud-application-secrets --query SecretString --output text)
if [ $? -ne 0 ]; then
    echo "Failed to retrieve secret from AWS Secrets Manager."
    exit 1
fi
export DB_PASSWORD=$(echo "$DB_PASSWORD_JSON" | jq -r '.DB_PASSWORD')

# Stop any existing Gunicorn service
pkill -f gunicorn || true

# Ensure dependencies are installed before starting the app
pip3 install --no-cache-dir -r requirements.txt

# Start Flask app using Gunicorn
echo "Starting Gunicorn server..."
gunicorn --bind 0.0.0.0:5000 banking_crud:app --daemon

echo "Flask application started successfully."
