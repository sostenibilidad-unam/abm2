import model
import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random
from time import sleep

parser = argparse.ArgumentParser(description='Setup simulation.')
parser.add_argument('--db', default='sqlite:///:memory:', help='DB URL, default: sqlite:///:memory:', required=True)
parser.add_argument('--sid', type=int, required=True)
parser.add_argument('--mode', default='sync')
parser.add_argument('--sleep', type=float, default=0.2)
args = parser.parse_args()


engine  = create_engine(args.db)
Session = sessionmaker(bind=engine)
session = Session()

model.session = session

s = session.query(model.SACMEX).get(args.sid)
s.status = 'play'
session.commit()
print "status set to play"

# as time goes by
while True:
    try:
        if args.mode == 'sync':
            s.repara_infras()
            s.t += 1
            print s.t
            session.commit()
            while session.query(model.AGEB).filter(model.AGEB.t != s.t).count()>0:
                sleep(args.sleep)
        else: # async
            s.repara_infras()
            session.commit()
            sleep(args.sleep)
    except KeyboardInterrupt:
        s.status = 'stop'
        session.commit()
        print "status set to stop"
        exit(0)

    session.refresh(s)
