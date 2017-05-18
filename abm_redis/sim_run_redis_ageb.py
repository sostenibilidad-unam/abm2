import argparse
import random
import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)
from Redis_AGEB import Redis_AGEB
from Redis_AGEB import umbral

parser = argparse.ArgumentParser(description='Welcome to the Redis version of the SACMEX simulation.')
parser.add_argument('-f', '--flush', help='Use if you want to start from anew. All Redis keys are flushed.', action='store_true')
parser.add_argument('-a', '--ageb', help='Use in conjunction with -f/--flush option to set number of AGEB agents. Defaults to 2000.', type=int, default=2000)
parser.add_argument('-i', '--iterations', help='Number of SACMEX iterations. Defaults to 5000.', type=int, default=5000)
args = parser.parse_args()

if args.flush:
	print 'Will now flush Redis.'
	r.flushall()
	# We set the SACMEX state to 1
	r.set('sacmex_t', 0)
	# Here we add new, empty AGEBs
	ageb_count = 0
	ageb = Redis_AGEB()
	while ageb_count < args.ageb:
		ageb.createNew()
		ageb_count += 1

sacmex_t = 0
while sacmex_t < args.iterations:
	sacmex_t += 1
	# We update the value for sacmex.
	r.set('sacmex_t', sacmex_t)
	# AGEB wear and tear
	ageb_count = 0
	ageb = Redis_AGEB()
	while ageb_count < args.ageb:
		ageb_count += 1
		ageb.getAGEB(ageb_count)
		ageb.runWearAndTear()
		ageb.save()
	# SACMEX will now repair broken AGEBs
	ageb_to_repair = r.zrevrange('ageb_reparar', 0, -1, True)
	for ageb_element in ageb_to_repair:
		repair = Redis_AGEB(ageb_element[0])
		# Repair wear and tear
		repair.deterioro = random.uniform(0.7, 0.8) * ageb_element[1]
		# If the repairs were sufficient, remove AGEB from list
		if repair.deterioro < umbral:
			repair.protestando = False
			r.zrem('ageb_reparar', ageb_element[0])
		repair.save()
