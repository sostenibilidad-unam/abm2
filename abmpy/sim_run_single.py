import model
import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random
from time import sleep
import timeit
from LimitMatrix import LimitMatrix

from pprint import pprint

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

l = LimitMatrix('../data/MC080416_OTR_bb.limit.csv')
ls = LimitMatrix('../data/sacmex_limit.csv')
s = session.query(model.SACMEX).get(args.sid)
for t in range(50):
    with session.begin():
        context = {
            'contaminacion_agua': {'max': 1, 'min': 0},
            'crecimiento_urbano': {'max': 1, 'min': 0},
            'desperdicio_agua': {'max': 1, 'min': 0},
            'desviacion_agua': {'max': 1, 'min': 0},
            'eficacia_servicio': {'max': 1, 'min': 0},
            'falta_infraestructura': {'max': session.query(model.AGEB).order_by(model.AGEB.faltain.desc()).first().faltain, 'min': 0},
            'obstruccion_alcantarillado': {'max': 1, 'min': 0},
            'escasez_agua': {'max': session.query(model.AGEB).order_by(model.AGEB.escasez.desc()).first().escasez, 'min': 0},
            'inundaciones': {'max': session.query(model.AGEB).order_by(model.AGEB.total_ench.desc()).first().total_ench, 'min': 0},
            'salud': {'max': session.query(model.AGEB).order_by(model.AGEB.disease_bu.desc()).first().disease_bu, 'min': 0},

            
            'edad_infra': {'max': session.query(model.AGEB).order_by(model.AGEB.edad_infra.desc()).first().edad_infra, 'min': 0},
            'capacidad': {'max': 1, 'min': 0},
            'fallain': {'max': session.query(model.AGEB).order_by(model.AGEB.fallain.desc()).first().fallain, 'min': 0},
            'presion_hidraulica': {'max': 1, 'min': 0},
            'monto': {'max': 1, 'min': 0},
            'calidad_agua': {'max': 1, 'min': 0},
            'abastecimiento': {'max': 1, 'min': 0},
            'peticion_delegaciones': {'max': session.query(model.AGEB).order_by(model.AGEB.petdels.desc()).first().petdels, 'min': 0},
            'presion_medios': {'max': session.query(model.AGEB).order_by(model.AGEB.presmed.desc()).first().presmed, 'min': 0},
            'presion_social': {'max': 1, 'min': 0}
            }

        s.limit_matrix = ls
        s.context = context
        pprint(s.get_maintenance_distances())
        s.step()
        for a in session.query(model.AGEB).all():
            a.limit_matrix = l
            a.context = context
            a.step()
            
        print t
