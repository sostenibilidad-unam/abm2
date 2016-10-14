java -Xmx8024m -cp ~/bin/netlogo/app/NetLogo.jar org.nlogo.headless.Main \
     --model ABM_V2.0.nlogo \
     --experiment prueba \
     --setup-file $1 \
     --table $2 \
     --threads $3
