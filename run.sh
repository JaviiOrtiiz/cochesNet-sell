#!/bin/bash
docker run -d -v /home/pablo/cochesNet-sell:/app --restart always cochesnet-sell --name cochesnet -p 5000:5000
