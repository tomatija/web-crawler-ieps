#!/bin/sh

# Run the setup script
python /app/setup_admin_user.py

# Start Flask
exec flask run --host=0.0.0.0 --port=5000
