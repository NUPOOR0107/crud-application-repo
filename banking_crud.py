import os
import json
import boto3
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

# AWS Secrets Manager settings
SECRET_NAME = "crud-application-secrets"  # Update this
AWS_REGION = "ap-southeast-1"  # Update with your AWS region

def get_db_credentials():
    """Retrieve database credentials from AWS Secrets Manager"""
    try:
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
    except Exception as e:
        print(f"Error fetching secrets: {str(e)}")
        return None

# Fetch database credentials
db_credentials = get_db_credentials()

# Database connection function
def get_db_connection():
    """Establish a database connection"""
    if not db_credentials:
        print("Database credentials not found.")
        return None

    try:
        conn = psycopg2.connect(
            host=db_credentials["host"],
            database=db_credentials["dbname"],
            user=db_credentials["user"],
            password=db_credentials["password"],
            port=db_credentials["port"]
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {str(e)}")
        return None

@app.route("/")
def home():
    return jsonify({"message": "Flask Banking App with PostgreSQL and AWS Secrets Manager!"})

@app.route("/customers")
def get_customers():
    """Fetch all customers from the database"""
    conn = get_db_connection()
    if not conn:
        return jsonify
