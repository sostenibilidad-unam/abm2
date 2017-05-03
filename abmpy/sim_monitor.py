import model
import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random


parser = argparse.ArgumentParser(description='Setup simulation.')
parser.add_argument('--db', default='sqlite:///:memory:', help='DB URL, default: sqlite:///:memory:')
parser.add_argument('--aid', type=int)
args = parser.parse_args()


engine  = create_engine(args.db)
Session = sessionmaker(bind=engine)
session = Session()

a = session.query(model.AGEB).get(args.aid)
    
print a
