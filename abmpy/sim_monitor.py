import model
import argparse
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from time import sleep


parser = argparse.ArgumentParser(description='Setup simulation.')
parser.add_argument('--db', default='sqlite:///:memory:', help='DB URL, default: sqlite:///:memory:')
parser.add_argument('--ids', type=int, nargs="+")
parser.add_argument('--sleep', type=float, default=0.3)
args = parser.parse_args()


engine  = create_engine(args.db)

@event.listens_for(engine, 'begin')
def receive_begin(conn):
        conn.execute('SET TRANSACTION READ ONLY')

        
Session = sessionmaker(bind=engine)
session = Session()

while True:
    print [session.query(model.AGEB).get(aid) for aid in args.ids]
    sleep(args.sleep)
