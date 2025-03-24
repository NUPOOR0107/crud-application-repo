import os
import json
import boto3
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

# AWS Secrets Manager settings
SECRET_NAME = "crud-application-secrets"  # Update this
AWS_REGION = "ap-southeast-1"  # e.g., us-east-1

def get_db_credentials():
    """Retrieve database credentials from AWS Secrets Manager"""
    client = boto3.client("secretsmanager", region_name=AWS_REGION)
    secret_value = client.get_secret_value(SecretId=SECRET_NAME)
    secret = json.loads(secret_value["SecretString"])
    
    return {
        "host": secret["host"],
        "dbname": secret["dbname"],
        "user": secret["username"],
        "password": secret["password"],
        "port": secret.get("port", "5432"),
    }

# Fetch database credentials
db_credentials = get_db_credentials()

# Database connection function
def get_db_connection():
    return psycopg2.connect(
        host=db_credentials["host"],
        database=db_credentials["dbname"],
        user=db_credentials["user"],
        password=db_credentials["password"],
        port=db_credentials["port"]
    )

@app.route("/")
def home():
    return jsonify({"message": "Flask Banking App with PostgreSQL and AWS Secrets Manager!"})

@app.route("/customers")
def get_customers():
    """Fetch all customers from the database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers")  # Update with your table name
        customers = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(customers)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
