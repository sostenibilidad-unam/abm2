import model
import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random
from time import sleep
import timeit
import value_function_dicts


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
for t in range(50):
    with session.begin():
        if t % 5:
            s.step()
        for a in session.query(model.AGEB).all():
            a.step()
            
        print t


