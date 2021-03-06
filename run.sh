#!/bin/bash

java -Xmx8024m -cp NetLogo.jar org.nlogo.headless.Main \
     --model ABM_V2.0.nlogo \
     --experiment experiment \
     --setup-file $1 \
     --table $2 \
     --threads $3
