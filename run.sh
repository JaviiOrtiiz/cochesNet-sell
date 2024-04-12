#!/bin/bash
docker run -d -v /home/pablo/cochesNet-sell:/app --restart always --name cochesnet-sell --privileged cochesnet-sell
