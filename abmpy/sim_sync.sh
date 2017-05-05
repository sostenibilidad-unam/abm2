DB=postgres+psycopg2://abm:abm@katsina1

source venv2/bin/activate

echo "initializing tables"
python sim_init.py --db $DB

sleep 1

echo "launching agent processes"
for i in {1..200}
do
    python sim_run_ageb.py --db $DB --aid $i --mode sync &
done

sleep 3

echo "starting simulation"
python sim_run_sacmex.py --db $DB --sid 1 --mode sync
