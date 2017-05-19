import model
import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random
from time import sleep
import timeit

parser = argparse.ArgumentParser(description='Setup simulation.')
parser.add_argument('--db', default='sqlite:///:memory:', help='DB URL, default: sqlite:///:memory:', required=True)
parser.add_argument('--sid', type=int, required=True)
parser.add_argument('--mode', default='sync')
parser.add_argument('--sleep', type=float, default=0.2)
args = parser.parse_args()


engine  = create_engine(args.db)
Session = sessionmaker(bind=engine, autocommit=True)
session = Session()

model.session = session

s = session.query(model.SACMEX).get(args.sid)
while True:
    with session.begin():
        s.repara_infras()
        s.t += 1
        for a in session.query(model.AGEB).all():
            a.deteriora()
            a.update_protesta()
        print s.t            


