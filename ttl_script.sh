#!/bin/bash

# Daily folder cleanup script
# This script clears all contents from a specified folder

# Configuration
FOLDER_PATH="~/code/audio-video-saver-be/downloads"  # Change this to your target folder
LOG_FILE="/var/log/folder_cleanup.log"

# Function to log messages with timestamp
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Check if folder exists
if [ ! -d "$FOLDER_PATH" ]; then
    log_message "ERROR: Folder $FOLDER_PATH does not exist"
    exit 1
fi

# Count files before cleanup (for logging)
file_count=$(find "$FOLDER_PATH" -type f | wc -l)
dir_count=$(find "$FOLDER_PATH" -mindepth 1 -type d | wc -l)

# Clear the folder contents
if [ "$(ls -A "$FOLDER_PATH")" ]; then
    rm -rf "$FOLDER_PATH"/*
    log_message "SUCCESS: Cleared $file_count files and $dir_count directories from $FOLDER_PATH"
else
    log_message "INFO: Folder $FOLDER_PATH was already empty"
fi

# Alternative safer approach (uncomment if you prefer):
# This moves files to a backup location before deletion
# BACKUP_DIR="/tmp/folder_backup_$(date +%Y%m%d_%H%M%S)"
# mkdir -p "$BACKUP_DIR"
# mv "$FOLDER_PATH"/* "$BACKUP_DIR" 2>/dev/null
# log_message "SUCCESS: Moved contents to backup at $BACKUP_DIR"