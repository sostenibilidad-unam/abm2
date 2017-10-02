
# Agent Based Model, Python version

This directory contains a rewrite of the ABM.

To run it you must install the requirements, perhaps within a virtualenv.

    # create virtual environment for python
    $ virtualenv venv
    # activate environment
    $ sourve venv/bin/activate
    # install requirements
    $ pip install -r requirements.txt


## Initialize simulation

First you must convert shp files into a set of queries. Like so:

    shp2pgsql -I -s 4326 /path/to/ageb.shp ageb -a > ageb.sql

Then you must edit that sql file and remove the table creation stanzas.
Table creation must be done through the ORM with the init script:

    # activate environment
    $ source venv/bin/activate
    # initialize simulation
    $ python sim_init.py --db postgresql+psycopg2://abm:abm@katsina1

Finally load the sql file, thusly:

    psql -U abm -W -d abm -h katsina1 -f ageb.sql


## Run simulation

    # activate environment
    $ source venv/bin/activate
    $ python sim_run_single.py --db postgresql+psycopg2://abm:abm@localhost