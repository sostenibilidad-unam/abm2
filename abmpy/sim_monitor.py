import model
import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from time import sleep


parser = argparse.ArgumentParser(description='Setup simulation.')
parser.add_argument('--db', default='sqlite:///:memory:', help='DB URL, default: sqlite:///:memory:')
parser.add_argument('--ids', type=int, nargs="+", required=True)
parser.add_argument('--sleep', type=float, default=0.3)
args = parser.parse_args()


engine  = create_engine(args.db)
        
Session = sessionmaker(bind=engine)
session = Session()

while True:
    print [session.query(model.AGEB).get(aid) for aid in args.ids]
    sleep(args.sleep)
