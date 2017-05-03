import model
import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random
from time import sleep

parser = argparse.ArgumentParser(description='Setup simulation.')
parser.add_argument('--db', default='sqlite:///:memory:', help='DB URL, default: sqlite:///:memory:', required=True)
parser.add_argument('--sid', type=int, required=True)
args = parser.parse_args()


engine  = create_engine(args.db)
Session = sessionmaker(bind=engine)
session = Session()

model.session = session

s = session.query(model.SACMEX).get(args.sid)
s.status = 'run'
session.commit()

# as time goes by
while True:
    try:
        if s.status == 'run':
            s.repara_infras()
            session.commit()
            sleep(1)
    except KeyboardInterrupt:
        s.status = 'stop'
        session.commit()
        exit(0)
    
    session.refresh(s)
