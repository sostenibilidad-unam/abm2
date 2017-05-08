import model
import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random


parser = argparse.ArgumentParser(description='Setup simulation.')
parser.add_argument('--db', help='DB URL', required=True)
parser.add_argument('--presupuesto', default=300)
parser.add_argument('--mode', help='reset or init', default='reset')
parser.add_argument('--agebs', default=2400, type=int)
args = parser.parse_args()


engine  = create_engine(args.db)
Session = sessionmaker(bind=engine)
session = Session()


if args.mode == 'reset':
    model.AGEB.__table__.drop(engine)
    model.SACMEX.__table__.drop(engine)

# setup orm
model.Base.metadata.create_all(engine)


# crear agebs
for n in range(args.agebs):
    a = model.AGEB(deterioro_infra=random.uniform(0.1,0.5),
                   protestante=False,
                   running_host=None,
                   t=0)
    session.add(a)
session.commit()

# crear sacmex
s = model.SACMEX(presupuesto=args.presupuesto,
                 status='pause',
                 t=0)
session.add(s)
session.commit()
