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

    def get_type(self):
        if self.kmeans5 == 2 or self.kmeans5 == 0:
            return 'iz'
        elif self.kmeans5 == 4:
            return 'mc'
        else:
            return 'xo'
    
    # acciones
    def accion_colectiva(self):
        pass
    
    def captacion_de_agua(self):
        self.escasez *= 0.8

    def compra_de_agua(self):
        self.escasez *= 0.8        

    def modificacion_de_vivienda(self):
        pass

    def movilizaciones(self):
        self.presmed *= 1.1
        self.protestant = True
        
        
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

        # al paso del tiempo hay deterioro
        self.edad_infra += random.uniform(1.0, 5.0)
        
        accion = self.decide()
        accion()
        


    def __repr__(self):
        return "<A%s>" % (self.gid)


class SACMEX:
    presupuesto_distribucion_agua = 100
    presupuesto_extraccion_agua = 100
    presupuesto_importacion_agua = 100
    presupuesto_mantenimiento = 100
    presupuesto_nueva_infraestructura = 100
    

    context = None
    limit_matrix = None

    # acciones
    def distribucion_agua(self):
        distances = self.get_distribucion_agua_distances()
        for ageb in sorted(distances, key=distances.__getitem__, reverse=True):
            if self.presupuesto_distribucion_agua > 0:
                # alterar ageb
                self.presupuesto_distribucion_agua -= 1

    
    def extraccion_agua(self):
        distances = self.get_extraccion_agua_distances()
        for ageb in sorted(distances, key=distances.__getitem__, reverse=True):
            if self.presupuesto_extraccion_agua > 0:
                # alterar ageb
                self.presupuesto_extraccion_agua -= 1

    
    def importacion_agua(self):
        distances = self.get_importacion_agua_distances()
        for ageb in sorted(distances, key=distances.__getitem__, reverse=True):
            if self.presupuesto_importacion_agua > 0:
                # alterar ageb
                self.presupuesto_importacion_agua -= 1

    
    def mantenimiento(self):
        distances = self.get_mantenimiento_distances()
        for ageb in sorted(distances, key=distances.__getitem__, reverse=True):
            if self.presupuesto_mantenimiento > 0:
                if random.choice([True, True, False, False, False, False, False]):
                    ageb.edad_infra *= 0.8
                    self.presupuesto_mantenimiento -= 1

        
    def nueva_infraestructura(self):
        distances = self.get_nueva_infraestructura_distances()
        for ageb in sorted(distances, key=distances.__getitem__, reverse=True):
            if self.presupuesto_nueva_infraestructura > 0:
                if random.choice([True, False, False, False]): 
                    ageb.faltain *= 0.8
                    self.presupuesto_nueva_infraestructura -= 1



    # distancias de agebs
    def get_mantenimiento_distances(self):
        return {a: salts.Mantenimiento(self.limit_matrix, self.context, a).get_distance()
                for a in session.query(AGEB).all()}
    
    def get_distribucion_agua_distances(self):
        return {a: salts.DistribucionAgua(self.limit_matrix, self.context, a).get_distance()
                for a in session.query(AGEB).all()}
    
    def get_extraccion_agua_distances(self):
        return {a: salts.ExtraccionAgua(self.limit_matrix, self.context, a).get_distance()
                for a in session.query(AGEB).all()}
    
    def get_importacion_agua_distances(self):
        return {a: salts.ImportacionAgua(self.limit_matrix, self.context, a).get_distance()
                for a in session.query(AGEB).all()}
    
    def get_nueva_infraestructura_distances(self):
        return {a: salts.NuevaInfraestructura(self.limit_matrix, self.context, a).get_distance()
                for a in session.query(AGEB).all()}


    def step(self):
        self.presupuesto_distribucion_agua = 3000
        self.presupuesto_extraccion_agua = 3000
        self.presupuesto_importacion_agua = 3000
        self.presupuesto_mantenimiento = 3000
        self.presupuesto_nueva_infraestructura = 3000

        
        self.mantenimiento()
#        self.distribucion_agua()
#        self.extraccion_agua()
#        self.importacion_agua()
        self.nueva_infraestructura()
        



    def reporta_presupuestos(self):
        return (self.presupuesto_distribucion_agua,
                self.presupuesto_extraccion_agua,
                self.presupuesto_importacion_agua,
                self.presupuesto_mantenimiento,
                self.presupuesto_nueva_infraestructura)





        
