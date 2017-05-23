# coding: utf-8

from sqlalchemy import Column, Integer, Float, Boolean, String
from sqlalchemy.ext.declarative import declarative_base
import random

import alternatives as alts
import sacmex_alternatives as salts

from pprint import pprint

session = None

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

    t = Column(Integer)
    limit_matrix = None

    # acciones
    def accion_colectiva(self):
        return(" accion_colectiva(self):")
    
    def captacion_de_agua(self):
        return(" captacion_de_agua(self):")

    def compra_de_agua(self):
        return(" compra_de_agua(self):")

    def modificacion_de_vivienda(self):
        return(" compra_infra_agua(self):")

    def movilizaciones(self):
        return(" reuso(self):")

        

    def deteriora(self):
        pass
        
    def decide(self):

        distances = {'accion_colectiva': alts.AccionColectiva(self.limit_matrix, self.context, self).get_distance(),
                     'captacion_de_agua': alts.CaptacionAgua(self.limit_matrix, self.context, self).get_distance(),
                     'compra_de_agua' :alts.CompraAgua(self.limit_matrix, self.context, self).get_distance(),
                     'modificacion_de_vivienda' :alts.ModificacionVivienda(self.limit_matrix, self.context, self).get_distance(),
                     'movilizaciones' :alts.Movilizaciones(self.limit_matrix, self.context, self).get_distance()}

        max_distance = sorted(distances, key=distances.__getitem__)[-1]
        
        if max_distance == 'accion_colectiva':
            accion = self.accion_colectiva
        elif max_distance == 'captacion_de_agua':
            accion = self.captacion_de_agua
        elif max_distance == 'compra_de_agua':
            accion = self.compra_de_agua
        elif max_distance == 'modificacion_de_vivienda':
            accion = self.modificacion_de_vivienda
        elif max_distance == 'movilizaciones':
            accion = self.movilizaciones
    
        return accion

        
    def step(self):

        accion = self.decide()
        accion()
        
        #
        self.deteriora()
        #self.update_protesta()


    def __repr__(self):
        return "<A%s>" % (self.gid)


class SACMEX(Base):
    __tablename__ = 'sacmex'
    id = Column(Integer, primary_key=True)
    status = Column(String) # play, pause, stop
    presupuesto = Column(Float)

    context = None
    limit_matrix = None

    # acciones
    def repara_infra(self, ageb):
        pass
    def distribucion_agua(self):
        pass
    def extraccion_agua(self):
        pass
    def importacion_agua(self):
        pass
    
    def mantenimiento(self):
        pass
        
    def nueva_infraestructura(self):
        pass



    def get_maintenance_distances(self):
        return {a: salts.Mantenimiento(self.limit_matrix, self.context, a).get_distance()
                for a in session.query(AGEB).all()}
            
    
    def __repr__(self):
        return "<SACMEX%s>" % self.id

    def step(self):
        #distancias_mant = [s.dist_mant(a) for a in agebs]
        pass









        
