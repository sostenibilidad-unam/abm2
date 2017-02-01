# Agent Based Modeling

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

## Run simulation thru ht-condor

Switch to the work directory and submit jobs to queue like this:

    $ cd /path/to/workdir
    $ condor_submit submit_all.condor

## Concat output

Output files can be concatenated with the following command:

    find /path/to/workdir -iname 'output_*csv' -exec tail -n +8 {} \; > /path/to/concat_output.csv


## Path to vegetation maps

https://www.dropbox.com/home/megadapt_integracion/insumos/agosto2016/inegi/USV/USV%20Serie%20V

The maps projection is UTM 14N WGS84
