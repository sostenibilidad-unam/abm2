import argparse

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

import random
import model

################################
# parse command line arguments #
################################
parser = argparse.ArgumentParser(description='Setup party simulation by creating and populating groups and guests.')
parser.add_argument('--db_url', default='sqlite:///:memory:', help='DB URL, default: sqlite:///:memory:')
parser.add_argument('--inittable', default='agebs_all_attributes', help='name of init table')
parser.add_argument('--sacmex_matrix', type=argparse.FileType('r'), required=True, help='path to SACMEX matrix')
parser.add_argument('--xochimilco_matrix', type=argparse.FileType('r'), required=True, help='path to Xochimilco matrix')
parser.add_argument('--iztapalapa_matrix', type=argparse.FileType('r'), required=True, help='path to Ixtapalapa matrix')
parser.add_argument('--contreras_matrix', type=argparse.FileType('r'), required=True, help='path to Contreras matrix')
args = parser.parse_args()

####################
# database connect #
####################
engine  = create_engine(args.db_url)



Session = sessionmaker(bind=engine)
session = Session()

# setup orm
model.Base.metadata.create_all(engine)
model.session=session

# drop everything for reset
session.query(model.AGEB).delete(synchronize_session='fetch')
session.query(model.Pozo).delete(synchronize_session='fetch')

conn = engine.connect()
s = text("select * from %s" % args.inittable)
for row in conn.execute(s).fetchall():
    ageb = dict(row)

    if  (ageb['kmeans5'] == 1) or (ageb['kmeans5'] == 3):
        residentMatrixPath = args.xochimilco_matrix.name
    elif (ageb['kmeans5'] == 2) or (ageb['kmeans5'] == 0):
        residentMatrixPath = args.iztapalapa_matrix.name
    elif (ageb['kmeans5'] == 4):
        residentMatrixPath = args.contreras_matrix.name
    else:
        continue
    
    a = model.AGEB(args.sacmex_matrix.name, residentMatrixPath)
    a.ID = ageb['ageb_id']
    a.poblacion = ageb['pobtot'] if ageb['pobtot'] > 0 else 1
    a.houses_with_abastecimiento = ageb['vph_aguadv'] / (1 + ageb['vph_aguadv'] + ageb['vph_aguafv'])
    a.houses_with_dranage = ageb['vph_drenaj']  / (1 + ageb['vph_drenaj']  + ageb['vph_nodren'] ) 
    a.hundimientos = ageb['hund']
    a.group_kmean = ageb['kmeans5']
    a.disease_burden = (ageb["n04_todas"] + ageb["x05_total"] + ageb["x06_todas"] + ageb["x07_todas"]+ ageb["x08_todas"]+ ageb["x09_todas"]+ ageb["n10_todas"]+ ageb["n11_todas"]+ ageb["n12_todas"] + ageb["n13_todas"] + ageb["n14_todas"]) / 11 
    a.income_index = 0 if ageb['i05_ingres'] == 'nobody' else ageb['i05_ingres'] #nobody????
    a.flooding = 0 if ageb['mean_encha'] == 'nobody' else ageb['mean_encha'] #?????????????????????????????'
    a.antiguedad_infra = ageb['edad_infra']
    a.zona_aquifera = ageb['zonas']
    
    
    session.add(a)
session.commit()


