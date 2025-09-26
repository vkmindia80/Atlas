#!/usr/bin/env python3
"""
Create a test authentication token for demo purposes
"""
import jwt
from datetime import datetime, timedelta

# Demo user data
user_data = {
    "user_id": "fa251190-44ce-4944-9830-7e45835d3f44",
    "tenant_id": "3853bd95-11ff-4ad9-8537-12099902aec7",
    "username": "demo",
    "email": "demo@example.com",
    "user_role": "project_manager",
    "exp": datetime.utcnow() + timedelta(hours=24)
}

# Use a simple secret key for demo
secret_key = "demo-secret-key-for-testing"

# Generate JWT token
token = jwt.encode(user_data, secret_key, algorithm='HS256')
print(f"Demo JWT Token: {token}")

# Also save to a file for easy access
with open('/tmp/demo_token.txt', 'w') as f:
    f.write(token)