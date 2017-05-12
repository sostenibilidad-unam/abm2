from ageb_ids import ageb_ids

plantilla = """
executable = /srv/home/rgarcia/abm2/abmpy/venv2/bin/python

arguments = sim_run_ageb.py --db {db} --ids {ids}

output    = r_{idss}.out
error     = r_{idss}.err
log       = r_{idss}.log

queue

"""

db="postgres+psycopg2://abm:abm@katsina1"

while len(ageb_ids) > 0:
    ids = []
    for n in range(5):
        try:
            ids.append(ageb_ids.pop())
        except:
            pass
    print plantilla.format(db=db,
                           ids=" ".join([str(i) for i in ids]),
                           idss="_".join([str(i) for i in ids]))
