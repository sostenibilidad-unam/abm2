plantilla = """
executable = /srv/home/rgarcia/abm2/abmpy/venv2/bin/python

arguments = sim_run_ageb.py --db {db} --ids {ids}

output    = r_{idss}.out
error     = r_{idss}.err
log       = r_{idss}.log

queue

"""

db="postgres+psycopg2://abm:abm@katsina1"

for i in range(480):
    ids = " ".join([str(i*5+j+1) for j in range(5)])
    idss = "_".join([str(i*5+j+1) for j in range(5)])    
    print plantilla.format(db=db, ids=ids, idss=idss)
