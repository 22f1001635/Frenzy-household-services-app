#!/bin/bash

# Function to run commands in the background
run_in_background() {
  local directory="$1"
  local command="$2"
  (
    cd "$directory" || exit
    eval "$command"
  ) &
}

# Run frontend commands in the background
run_in_background "frontend" "npm run build && npm run dev"

# Run backend commands in the background
run_in_background "backend" "flask run"

# Notify user and keep the script's terminal open
echo "Frontend and backend processes started. Check the respective terminal outputs."
read -p "Press Enter to exit this terminal."