# coding: utf-8

from sqlalchemy import Column, Integer, ForeignKey, Float, Boolean, String
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random
#import pandas as pd

Base = declarative_base()


class AGEB(Base):
    __tablename__ = 'agebs'
    id = Column(Integer, primary_key=True)    

#    distancia = Column(Float)

    deterioro_infra = Column(Float)
    protestante = Column(Boolean)

    def update_protesta(self):
        if random.random() < self.deterioro_infra:
            self.protestante = True
        else:
            self.protestante = False
            
    def deteriora(self):
        if self.deterioro_infra < 1.0:
            self.deterioro_infra = random.uniform(1.01, 1.1) * self.deterioro_infra
#            session.add(self)
#            session.commit()

    def accion_colectiva(self):
        if self.deteriora_infra > 0:
            self.deterioro_infra = random.uniform(0.9, 1) * self.deterioro_infra

    def repara_infra(self, cuanto):
        self.deterioro_infra -= cuanto

    def __repr__(self):
        if self.protestante:
            return "<A%s! %s>" % (self.id, self.deterioro_infra)
        else:
            return "<A%s %s>" % (self.id, self.deterioro_infra)
#    def update_distancia(self):
#        self.distancia = random.random()
    


class SACMEX(Base):
    __tablename__ = 'sacmex'
    id = Column(Integer, primary_key=True)    

    presupuesto = Column(Float)

    status = Column(String)
    
    def repara_infras(self):
        for a in session.query(AGEB).filter(AGEB.protestante==True).order_by(AGEB.deterioro_infra.asc()).all():
            self.repara_infra(a)
    
    def repara_infra(self, ageb):
        if self.presupuesto > 0:        
            cuanto = random.uniform(0.7, 0.8) * ageb.deterioro_infra
            ageb.repara_infra(cuanto)
            self.presupuesto -= 1
            session.commit()

    def __repr__(self):
        return "<SACMEX%s>" % self.id







