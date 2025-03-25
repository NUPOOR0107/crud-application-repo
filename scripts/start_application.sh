#!/bin/bash
set -e  # Exit if any command fails

echo "Starting Flask application..."

cd /home/ec2-user/banking_crud || exit 1

# Load environment variables from AWS Secrets Manager
export DB_HOST="banking-db-tht.ctgu00g8ckle.ap-southeast-1.rds.amazonaws.com"
export DB_NAME="bankingdb"
export DB_USER="thtadmin"

# Fetch DB password securely
DB_PASSWORD_JSON=$(aws secretsmanager get-secret-value --secret-id crud-application-secrets --query SecretString --output text)
if [ $? -ne 0 ]; then
    echo "❌ Failed to retrieve secret from AWS Secrets Manager."
    exit 1
fi
export DB_PASSWORD=$(echo "$DB_PASSWORD_JSON" | jq -r '.password')

# Stop any existing Gunicorn service
echo "🔄 Stopping existing Gunicorn process (if any)..."
pkill -f gunicorn || true
sleep 2  # Ensure process stops

# Activate virtual environment if exists
if [ -d "venv" ]; then
    echo "✅ Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️ No virtual environment found, using system Python."
fi

# Ensure dependencies are installed
echo "📦 Installing dependencies..."
pip3 install --no-cache-dir -r requirements.txt

# Start Flask app using Gunicorn with logging
echo "🚀 Starting Gunicorn server..."
gunicorn --bind 0.0.0.0:5000 banking_crud:app --daemon --log-file gunicorn.log --error-logfile error.log --capture-output --enable-stdio-inheritance

echo "✅ Flask application started successfully."

# Log process info
ps aux | grep gunicorn
