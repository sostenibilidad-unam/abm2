import model

#activate_this = '/srv/home/rgarcia/abm2/abmpy/venv2/bin/activate_this.py'
#execfile(activate_this, dict(__file__=activate_this))

import argparse
import random
from time import sleep

parser = argparse.ArgumentParser(description='Setup simulation.')
#parser.add_argument('--db', default='sqlite:///:memory:', help='DB URL, default: sqlite:///:memory:')
#parser.add_argument('--mode', default='sync')
parser.add_argument('--ids', type=int, nargs="+", required=True)
parser.add_argument('--sleep', type=float, default=0.1)
args = parser.parse_args()

agebs = [model.AGEB(pk=k) for k in args.ids]

s = model.SACMEX(pk=1)

# as time goes by

while True:
    if s.status == 'play':
        for a in agebs:
            if a.t != s.t:
                a.sync_run(s.t)
    if s.status == 'stop':
        break

    sleep(args.sleep)
    s = model.SACMEX(pk=1)
