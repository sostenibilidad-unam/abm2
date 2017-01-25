# Agent Based Modeling

To run from the command line interface try:

    $ ./run.sh setup.xml output.csv $threads

## Create cluster run files

This script will create a setup.xml file for every scenario in the CSV file. Run it like this:

    python vhu.py --argumentspace sampling_scenarios_new_Weights.csv
                  --landscape many-hills 
                  --new_infra_investment 40 
                  --maintenance 130 
                  --threads 8 
                  --netlogo /path/to/bin/netlogo-5.3.1-64 
                  --workdir /path/to/workdir

Setup files and a ht-condor submit file are created in "workdir".

Output files can be concatenated with the following command:

    find /path/to/workdir -iname 'output_*csv' -exec tail -n +8 {} \; > /path/to/concat_output.csv
