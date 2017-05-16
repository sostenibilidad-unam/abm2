activate_this = '/srv/home/rgarcia/abm2/abmpy/venv2/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import model
import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random
from time import sleep

parser = argparse.ArgumentParser(description='Setup simulation.')
parser.add_argument('--db', default='sqlite:///:memory:', help='DB URL, default: sqlite:///:memory:')
parser.add_argument('--mode', default='sync')
parser.add_argument('--ids', type=int, nargs="+", required=True)
parser.add_argument('--sleep', type=float, default=0.1)
args = parser.parse_args()

engine  = create_engine(args.db)
Session = sessionmaker(bind=engine)
session = Session()

agebs = [session.query(model.AGEB).get(aid) for aid in args.ids]

s = session.query(model.SACMEX).get(1)

# as time goes by
if args.mode=='sync':
    while True:
        if s.status == 'play':
            for a in agebs:
                if a.t != s.t:
                    a.sync_run(s.t)
                    session.commit()
        if s.status == 'stop':
            break

        sleep(args.sleep)
        session.refresh(s)
else:
    while True:
        if s.status == 'play':
            for a in agebs:
                a.async_run()
                session.commit()
        if s.status == 'stop':
            break

        sleep(args.sleep)
        session.refresh(s)


