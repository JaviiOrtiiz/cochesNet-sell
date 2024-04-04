#!/bin/bash

sh /home/pablo/mnt/mount.sh

# Copy the content of /home/pablo/cochesNet-sell/csv to /home/pablo/mnt/gdrive/
cp -r /home/pablo/cochesNet-sell/csv/* /home/pablo/mnt/gdrive/

# Check if the copy was successful
if [ $? -eq 0 ]; then
    echo "Copy successful!"
else
    echo "Error: Copy failed."
fi
