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
parser.add_argument('--inittable', default='ageb8', help='name of init table')
parser.add_argument('--sacmex_matrix', type=argparse.FileType('r'), required=True, help='path to SACMEX matrix')
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
    a = model.AGEB(args.sacmex_matrix.name)
    a.ID = ageb['ageb_id']
    a.poblacion = ageb['POBTOT'] if ageb['POBTOT'] > 0 else 1
    a.houses_with_abastecimiento = ageb['VPH_AGUADV'] / (1 + ageb['VPH_AGUADV'] + ageb['VPH_AGUAFV'])
    a.houses_with_dranage = ageb['VPH_DRENAJ']  / (1 + ageb['VPH_DRENAJ']  + ageb['VPH_NODREN'] ) 
    ## a.hundimientos = ageb['HUND']
    ##a.group_kmean = ageb['KMEANS5']
    a.disease_burden = (ageb["N04_TODAS"] + ageb["X05_TOTAL"] + ageb["X06_TODAS"] + ageb["X07_TODAS"]+ ageb["X08_TODAS"]+ ageb["X09_TODAS"]+ ageb["N10_TODAS"]+ ageb["N11_TODAS"]+ ageb["N12_TODAS"] + ageb["N13_TODAS"] + ageb["N14_TODAS"]) / 11 
    a.income_index = 0 if ageb['I05_INGRES'] == 'nobody' else ageb['I05_INGRES']
    ##a.flooding = 0 if ageb['Mean_encha'] == 'nobody' else ageb['Mean_encha']
    ##a.antiguedad_infra = ageb['edad_infra']
    ##a.zona_aquifera = ageb['zonas']
    
    session.add(a)
session.commit()


