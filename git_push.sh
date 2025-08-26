#!/bin/bash

# Prompt for a commit message
echo "Enter your commit message:"
read commit_message

# Prompt for the branch name
echo "Enter the branch name to push to:"
read branch_name

# Git commands
git status
git add .
git commit -m "$commit_message"
git push origin "$branch_name"
