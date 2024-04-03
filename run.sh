#!/bin/bash
docker run -d -v /home/pablo/cochesNet-sell:/app --restart always cochesnet-sell --name cochesnet-sell -p 5000:5000
