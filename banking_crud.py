import os
import json
import boto3
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

# AWS Secrets Manager settings
SECRET_NAME = "crud-application-secrets"
AWS_REGION = "ap-southeast-1"

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

# ✅ GET Endpoint: Fetch current balance
@app.route("/balance/<int:customer_id>", methods=["GET"])
def get_balance(customer_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM customers WHERE id = %s", (customer_id,))
        result = cursor.fetchone()
        
        if result:
            balance = result[0]
            response = {"customer_id": customer_id, "balance": balance}
        else:
            response = {"error": "Customer not found"}

        cursor.close()
        conn.close()
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)})

# ✅ POST Endpoint: Deposit or Withdraw Money
@app.route("/transaction", methods=["POST"])
def transaction():
    try:
        data = request.get_json()
        customer_id = data.get("customer_id")
        amount = data.get("amount")
        transaction_type = data.get("transaction_type")  # "deposit" or "withdraw"

        if not customer_id or not amount or not transaction_type:
            return jsonify({"error": "Missing required fields"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Get current balance
        cursor.execute("SELECT balance FROM customers WHERE id = %s", (customer_id,))
        result = cursor.fetchone()

        if not result:
            return jsonify({"error": "Customer not found"}), 404

        current_balance = result[0]

        if transaction_type == "deposit":
            new_balance = current_balance + amount
        elif transaction_type == "withdraw":
            if amount > current_balance:
                return jsonify({"error": "Insufficient funds"}), 400
            new_balance = current_balance - amount
        else:
            return jsonify({"error": "Invalid transaction type"}), 400

        # Update balance in DB
        cursor.execute("UPDATE customers SET balance = %s WHERE id = %s", (new_balance, customer_id))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"customer_id": customer_id, "new_balance": new_balance, "transaction_type": transaction_type})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
