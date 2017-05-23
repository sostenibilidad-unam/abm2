# coding: utf-8

from sqlalchemy import Column, Integer, ForeignKey, Float, Boolean, String
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


import random
import pandas as pd

from pprint import pprint

import value_functions_per_alternative as vf_alt

Base = declarative_base()


def ideal_distance(alpha, criteria, criteria_weights, exponent):
    """
    this function calcualtes a distance to ideal point using compromized programing metric
    arguments:
    - VF_list: a list of value functions
    - weight_list a list of weights from the alternatives criteria links (CA_links)
    - h_Cp to control the type of distance h_Cp=2 euclidian; h_Cp=1 manhattan
    """
    return alpha * sum([(criteria[n] * criteria_weights[n]) ** float(exponent)
                         for n in range(len(criteria))]) ** (1 / float(exponent))


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
        if self.d_infra < 1.0:
            self.d_infra = random.uniform(1.01, 1.1) * self.d_infra


    def get_distancia(self, alpha, vf, criteria):
        """
        vf is a dictionary of value functions, defined in value_functiion_dicts
        criteria is a list of criteria keys that must also be class attibutes
        """
        v = [vf[criterion](self.__dict__[criterion]) for criterion in criteria]

        return ideal_distance(alpha,
                              v,
                              self.limit_matrix.criteria.values(),
                              2)


    # crit_catp_agua=
    # vf=vf.capt_agua
    # get_distancia(vf, crit_capt_agua)
        
    def decide(self):

        accion_colectiva = ['escasez', 'edad_infra', 'total_ench', 'faltain', 'escasez', 'disease_bu']
        captacion_de_agua = ['escasez', 'edad_infra', 'total_ench', 'faltain', 'escasez', 'disease_bu']
        compra_de_agua = ['escasez', 'edad_infra', 'total_ench', 'faltain', 'escasez', 'disease_bu']
        modificacion_de_vivienda = ['escasez', 'edad_infra', 'total_ench', 'faltain', 'escasez', 'disease_bu']
        movilizaciones = ['escasez', 'edad_infra', 'total_ench', 'faltain', 'escasez', 'disease_bu']

        distances = {
            'accion_colectiva': self.get_distancia(self.limit_matrix.alternatives['accion_colectiva'],
                                                   vf_alt.accion_colectiva,
                                                   accion_colectiva),
            'captacion_de_agua': self.get_distancia(self.limit_matrix.alternatives['captacion_de_agua'],
                                                    vf_alt.captacion_de_agua,
                                                    captacion_de_agua),
            'compra_de_agua': self.get_distancia(self.limit_matrix.alternatives['compra_de_agua'],
                                                 vf_alt.compra_de_agua,
                                                 compra_de_agua),
            'modificacion_de_vivienda': self.get_distancia(self.limit_matrix.alternatives['modificacion_de_vivienda'],
                                                    vf_alt.modificacion_de_vivienda,
                                                    modificacion_de_vivienda),
            'movilizaciones': self.get_distancia(self.limit_matrix.alternatives['movilizaciones'],
                                        vf_alt.movilizaciones,
                                        movilizaciones)
            }

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

    # distancias

    def dist_mant(self, ageb):
        """
        compute distance to ideal maintenance
        """
        distance = value_function(random.random())
        return distance


    def update_criteria_max(self):
        self.criteria_max = {
            'antiguedad_infra': session.query(AGEB).order_by(AGEB.antiguedad_infra.desc()).first().antiguedad_infra,
            'capacidad': session.query(AGEB).order_by(AGEB.capacidad.desc()).first().capacidad,
            'falla': session.query(AGEB).order_by(AGEB.falla.desc()).first().falla,
            'falta': session.query(AGEB).order_by(AGEB.falta.desc()).first().falta,
            'presion_hidraulica': session.query(AGEB).order_by(AGEB.presion_hidraulica.desc()).first().presion_hidraulica,
            'monto': session.query(AGEB).order_by(AGEB.monto.desc()).first().monto,
            'water_quality': session.query(AGEB).order_by(AGEB.water_quality.desc()).first().water_quality,
            'scarcity': session.query(AGEB).order_by(AGEB.scarcity.desc()).first().scarcity,
            'flooding': session.query(AGEB).order_by(AGEB.flooding.desc()).first().flooding,
            'abastecimiento': session.query(AGEB).order_by(AGEB.abastecimiento.desc()).first().abastecimiento,
            'peticion_delegaciones' : 1, # TODO
            'presion_de_medios': 1,
            'presion_social': session.query(AGEB).order_by(AGEB.presion_social.desc()).first().presion_social
            }


    def step(self):
        s.update_criteria_max()
        distancias_mant = [s.dist_mant(a) for a in agebs]
        
        self.t += 1








        
