import model
import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random


parser = argparse.ArgumentParser(description='Setup simulation.')
parser.add_argument('--db', help='DB URL', required=True)
parser.add_argument('--mode', help='reset or init', default='reset')
args = parser.parse_args()

engine  = create_engine(args.db)
Session = sessionmaker(bind=engine)
session = Session()

if args.mode == 'reset':
    model.AGEB.__table__.drop(engine)
    model.SACMEX.__table__.drop(engine)

# setup orm
model.Base.metadata.create_all(engine)

# crear sacmex
s = model.SACMEX(presupuesto=1000)
session.add(s)
session.commit()
