import model
import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random


parser = argparse.ArgumentParser(description='Setup simulation.')
parser.add_argument('--db', help='DB URL', required=True)
parser.add_argument('--presupuesto', default=300)
args = parser.parse_args()


engine  = create_engine(args.db)
Session = sessionmaker(bind=engine)
session = Session()


# setup orm
model.Base.metadata.create_all(engine)



# crear 2400 agebs
for n in range(100):
    a = model.AGEB(deterioro_infra=random.uniform(0.1,0.8), protestante=False)
    session.add(a)
    session.commit()

# crear sacmex
s = model.SACMEX(presupuesto=args.presupuesto)
session.add(s)
session.commit()
