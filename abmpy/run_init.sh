DB=postgres+psycopg2://abm:abm@katsina1

source venv2/bin/activate

echo "initializing tables"
python sim_init.py --db $DB --agebs 2400
