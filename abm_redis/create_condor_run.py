plantilla = """
executable = /srv/home/opalacios/abm2/abm_redis/venv/bin/python

arguments = sim_run_ageb.py --ids {ids} --sleep 0.05

queue

"""

ageb_ids = range(1, 2433)

while len(ageb_ids) > 0:
    ids = []
    for n in range(5):
        try:
            ids.append(ageb_ids.pop())
        except:
            pass
    print plantilla.format(ids=" ".join([str(i) for i in ids]))
                           
