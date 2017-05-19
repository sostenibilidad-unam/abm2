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
    __tablename__ = 'ageb13_a'

    gid = Column(Integer, primary_key=True)

    cvegeo = Column(String)
    pobtot = Column(Integer)
    vph_aguadv = Column(Float)
    vph_aguafv = Column(Float)
    vph_drenaj = Column(Float)
    vph_nodren = Column(Float)
    total_ench = Column(Float)
    mean_encha = Column(Float)
    kmeans5 = Column(Integer)
    precip = Column(Integer)
    hund = Column(Float)
    edad_infra = Column(Float)
    zonas = Column(Float)
    i05_ingres = Column( Float)
    ageb_id = Column(Float)
    fallain = Column(Float)
    presmed = Column(Float)
    faltain = Column(Float)
    petdels = Column(Float)
    escasez = Column(Float)
    subside = Column(Float)
    disease_bu = Column(Float)
    protestant = Column(Boolean)
    d_infra = Column(Float)
    host = Column(String)
    
    t = Column(Integer)

    def update_protesta(self):
        if random.random() < self.d_infra:
            self.protestant = True
        else:
            self.protestant = False

    def deteriora(self):
        if self.d_infra < 1.0:
            self.d_infra = random.uniform(1.01, 1.1) * self.d_infra

    def accion_colectiva(self):
        if self.deteriora_infra > 0:
            self.d_infra = random.uniform(0.9, 1) * self.d_infra

    def repara_infra(self, cuanto):
        self.d_infra -= cuanto


    def sync_run(self, t):
        self.deteriora()
        self.update_protesta()
        self.t = t

    def async_run(self):
        self.deteriora()
        self.update_protesta()


    def __repr__(self):
        if self.protestant:
            return "<A%s! %0.2f t=%s>" % (self.gid, self.d_infra, self.t)
        else:
            return "<A%s  %0.2f t=%s>" % (self.gid, self.d_infra, self.t)



class SACMEX(Base):
    __tablename__ = 'sacmex'
    id = Column(Integer, primary_key=True)

    status = Column(String) # play, pause, stop

    t = Column(Integer)

    def repara_infras(self):
        for a in session.query(AGEB).filter(AGEB.protestant==True).all():
            self.repara_infra(a)

    def repara_infra(self, ageb):
        cuanto = random.uniform(0.7, 0.8) * ageb.d_infra
        ageb.repara_infra(cuanto)

    def __repr__(self):
        return "<SACMEX%s>" % self.id
