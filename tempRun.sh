#!/bin/bash

# Variables
LOCAL_DIRECTORY="./"  # Current directory on your local machine to save the file
CONTAINER_DIRECTORY="/app"  # Directory inside the container where the file is saved (adjust if necessary)
IMAGE_NAME="dining-web-scraping"  # Docker image name
CONTAINER_NAME="dining-web-scraping-container"  # Container name (you can modify this if needed)

# Step 1: Build the Docker image
echo "Building Docker image: $IMAGE_NAME"
docker build -t $IMAGE_NAME .

# Step 2: Run the Docker container
echo "Running Docker container: $CONTAINER_NAME"
docker run --name $CONTAINER_NAME $IMAGE_NAME

# Step 3: Wait for the container to finish and copy the file from the container (adjust the file name as needed)
# Assuming the file you want is a screenshot (screenshot.png) inside the container at /app
echo "Copying screenshot from container to local machine..."
docker cp $CONTAINER_NAME:$CONTAINER_DIRECTORY/screenshot.png $LOCAL_DIRECTORY/screenshot.png

# Step 4: Remove the container once it's done
echo "Removing Docker container: $CONTAINER_NAME"
docker rm $CONTAINER_NAME

echo "File has been copied to $LOCAL_DIRECTORY/screenshot.png"
