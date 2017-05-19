from ageb_ids import ageb_ids

# plantilla = """
# executable = /srv/home/rgarcia/abm2/abmpy/venv2/bin/python

# arguments = sim_run_ageb.py --db {db} --ids {ids} --sleep 0.5

# output    = r_{idss}.out
# error     = r_{idss}.err
# log       = r_{idss}.log

# requirements = TARGET.Machine=="katsina1.lancis.ecologia.unam.mx"

# queue

# """


head = """
executable = /srv/home/rgarcia/abm2/abmpy/venv2/bin/python
requirements = TARGET.Machine=="katsina1.lancis.ecologia.unam.mx"
"""

plantilla = """
arguments = sim_run_ageb.py --db {db} --ids {ids} --sleep 0.1
queue

"""



print head

db="postgres+psycopg2://abm:abm@katsina1"

ageb_ids = range(1, 2433)

while len(ageb_ids) > 0:
    ids = []
    for n in range(304):
        try:
            ids.append(ageb_ids.pop())
        except:
            pass
    print plantilla.format(db=db,
                           ids=" ".join([str(i) for i in ids]))
