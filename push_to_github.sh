#!/bin/bash

# Script to push to GitHub
# Usage: ./push_to_github.sh YOUR_GITHUB_USERNAME REPO_NAME

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: ./push_to_github.sh YOUR_GITHUB_USERNAME REPO_NAME"
    echo ""
    echo "First, create a new repository on GitHub:"
    echo "1. Go to https://github.com/new"
    echo "2. Enter repository name (e.g., doordash-bot)"
    echo "3. Don't initialize with README, .gitignore, or license"
    echo "4. Click 'Create repository'"
    echo ""
    echo "Then run this script with:"
    echo "./push_to_github.sh YOUR_USERNAME REPO_NAME"
    exit 1
fi

GITHUB_USER=$1
REPO_NAME=$2

echo "Adding remote origin..."
git remote add origin https://github.com/${GITHUB_USER}/${REPO_NAME}.git 2>/dev/null || git remote set-url origin https://github.com/${GITHUB_USER}/${REPO_NAME}.git

echo "Pushing to GitHub..."
git branch -M main
git push -u origin main

echo "Done! Your repository is now at: https://github.com/${GITHUB_USER}/${REPO_NAME}"

