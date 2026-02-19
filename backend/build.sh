#!/usr/bin/env bash
# Render build script for DateKeeper backend

set -o errexit  # Exit on error

echo "🔧 Starting build process..."

# Upgrade pip and install build tools first
echo "📦 Installing build tools..."
pip install --upgrade pip setuptools wheel

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Verify critical packages
echo "✅ Verifying installations..."
python verify_install.py

echo "✅ Build completed successfully!"
