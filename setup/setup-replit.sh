#!/bin/bash

# Install Python dependencies
echo "Installing Python dependencies..."
poetry config virtualenvs.in-project true
poetry install

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
yarn install

# Initialize PostgreSQL database
echo "Initializing PostgreSQL..."
createdb journal_db

# Run database migrations
echo "Running database migrations..."
psql -d journal_db -f setup/init-db.sql

# Create .env file from example if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

echo "Setup complete! Don't forget to update your .env file with your actual credentials." 