#!/bin/bash

echo "Cron Task Starting"

# Absolute path to docker-compose folder
COMPOSE_DIR="/home/pphyo/bitezone/web-scraping"

# Base logs directory (absolute)
BASE_LOG_DIR="/home/pphyo/bitezone/logs"

# Navigate to the docker-compose folder
cd "$COMPOSE_DIR" || { echo "Failed to cd into $COMPOSE_DIR"; exit 1; }

# Create folder for today's date
TODAY=$(date +"%Y-%m-%d")
LOG_DIR="$BASE_LOG_DIR/$TODAY"
mkdir -p "$LOG_DIR"

# Timestamp for this run
TIME=$(date +"%H-%M-%S")
STDOUT_LOG="$LOG_DIR/scraper_${TIME}_out.log"
STDERR_LOG="$LOG_DIR/scraper_${TIME}_err.log"

echo "Starting Docker Compose"
/usr/local/bin/docker-compose --env-file="$COMPOSE_DIR/.env" up > "$STDOUT_LOG" 2> "$STDERR_LOG"

echo "Operation Done. Ending Docker Compose"
/usr/local/bin/docker-compose down
