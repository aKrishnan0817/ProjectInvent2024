#!/bin/bash
REPO_PATH="/home/pptprojectinvent/ProjectInvent2024"
FLASK_APP_PATH="/home/pptprojectinvent/mysite"
SUBFOLDER="flask_app"

# Navigate to the repository
cd "$REPO_PATH"

# Copy the Flask app content to the subfolder
rsync -av --exclude='.git' --exclude='sensitiveData.py' "$FLASK_APP_PATH/" "$REPO_PATH/$SUBFOLDER/"

# Add changes to git
git add .

# Commit changes
git commit -m "Update Flask app content"

# Push to GitHub
git push origin main
