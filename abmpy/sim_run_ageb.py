import model
import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random
from time import sleep
from socket import gethostname

parser = argparse.ArgumentParser(description='Setup simulation.')
parser.add_argument('--db', default='sqlite:///:memory:', help='DB URL, default: sqlite:///:memory:')
parser.add_argument('--mode', default='sync')
parser.add_argument('--agebs', type=int, default=5)
parser.add_argument('--sleep', type=float, default=0.1)
args = parser.parse_args()


def set_running_host(host):
    for a in agebs:
        a.running_host = host
        session.add(a)

    session.commit()


engine  = create_engine(args.db)
Session = sessionmaker(bind=engine)
session = Session()

agebs = session.query(model.AGEB).filter(model.AGEB.running_host==None).limit(args.agebs).all()

set_running_host(gethostname())

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

set_running_host(None)
