import model
import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random
from time import sleep

parser = argparse.ArgumentParser(description='Setup simulation.')
parser.add_argument('--db', default='sqlite:///:memory:', help='DB URL, default: sqlite:///:memory:')
parser.add_argument('--aid', type=int)
args = parser.parse_args()


engine  = create_engine(args.db)
Session = sessionmaker(bind=engine)
session = Session()

a = session.query(model.AGEB).get(args.aid)

# as time goes by
for t in range(100):
    # pasa el tiempo para los agebs
    a.deteriora()
    a.update_protesta()
    session.commit()
    sleep(0.1)
