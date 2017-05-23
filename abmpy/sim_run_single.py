import model
import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random
from time import sleep
import timeit
import value_function_dicts
from LimitMatrix import LimitMatrix

parser = argparse.ArgumentParser(description='Setup simulation.')
parser.add_argument('--db', default='sqlite:///:memory:', help='DB URL, default: sqlite:///:memory:', required=True)
parser.add_argument('--sid', type=int, required=True)
parser.add_argument('--mode', default='sync')
parser.add_argument('--sleep', type=float, default=0.2)
args = parser.parse_args()


engine  = create_engine(args.db)
Session = sessionmaker(bind=engine, autocommit=True)
session = Session()

model.session = session

l = LimitMatrix('/path/to/lm')

s = session.query(model.SACMEX).get(args.sid)
for t in range(50):
    with session.begin():
        context = {
            'contaminacion_agua': {'max': 1, 'min': 0},
            'crecimiento_urbano': {'max': 1, 'min': 0},
            'desperdicio_agua': {'max': 1, 'min': 0},
            'desviacion_agua': {'max': 1, 'min': 0},
            'eficacia_servicio': {'max': 1, 'min': 0},
            'falta_infraestructura': {'max': session.query(AGEB).order_by(AGEB.faltain.desc()).first().faltain, 'min': 0},
            'obstruccion_alcantarillado': {'max': 1, 'min': 0},
            'escasez_agua': {'max': session.query(AGEB).order_by(AGEB.escasez.desc()).first().escasez, 'min': 0},
            'inundaciones': {'max': session.query(AGEB).order_by(AGEB.total_ench.desc()).first().total_ench, 'min': 0},
            'salud': {'max': session.query(AGEB).order_by(AGEB.disease_bu.desc()).first().disease_bu, 'min': 0},
            }
        if t % 5:
            s.step()
        for a in session.query(model.AGEB).all():
            a.limit_matrix = l
            a.context = context
            a.step()
            
        print t
