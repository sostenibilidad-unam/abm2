DB=postgres+psycopg2://abm:abm@katsina1

source venv2/bin/activate

python sim_monitor.py --db $DB --ids 3 5 15 22
