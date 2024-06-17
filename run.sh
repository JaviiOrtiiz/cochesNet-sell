#!/bin/bash
docker run -d -v /home/orangepi/cochesNet-sell:/app --restart always --name cochesnet-sell --privileged cochesnet-sell
