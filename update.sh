#!/bin/bash

# Navigate to the directory containing your repository
cd /home/orangepi/cochesNet-sell

# Pull the latest changes from the Git repository
git pull

# Stop and remove the old container if it exists
if [ "$(docker ps -q -f name=cochesnet-sell)" ]; then
    docker stop cochesnet-sell
    docker rm cochesnet-sell
fi

# Remove the old Docker image if it exists
if [ "$(docker images -q cochesnet-sell)" ]; then
    docker rmi cochesnet-sell
fi

# Build the Docker image
docker build -t cochesnet-sell .

# Run the run.sh script
sh run.sh
