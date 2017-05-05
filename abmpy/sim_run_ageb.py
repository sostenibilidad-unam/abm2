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
s = session.query(model.SACMEX).get(1)
# as time goes by
while True:
    if s.status == 'play':
        # pasa el tiempo para los agebs
        if a.t != s.t:
            a.run_to(s.t)        
            session.commit()
    if s.status == 'stop':
        break
    
    sleep(0.1)    
    session.refresh(s)
