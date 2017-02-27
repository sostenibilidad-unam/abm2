# coding: utf-8

from sqlalchemy import Column, Integer, ForeignKey, Float, Boolean, String
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.ext.declarative import declarative_base
import random

Base = declarative_base()

class AGEB(Base):
    __tablename__ = 'agebs'
    id = Column(Integer, primary_key=True)

    # relationships
    pozos = relationship("Pozo", back_populates="ageb")
    
    #paches_set_agebs = Column() #the set of patches that bellow to the ageb
        
    # attributes
    group_kmean = Column(Integer) # define to witch group an ageb belongs to, based on sosio-economic charactersitics
    zona_aquifera = Column(Integer)
    name_delegation = Column(String) #the name of the delegation the ageb belongs to

    Monto = Column(Float) # resources designated to each ageb (delegations?)
    production_water_perageb = Column(Float) # produccion de agua {definir escala e.g resolucion temporal !!!!}
    abastecimiento = Column(Float) #Necesidad de la población en cuanto a servicios hidráulicos (agua potable, drenaje)
    abastecimiento_b = Column(Float)
    antiguedad_infra = Column(Integer) #mean age of wells in ageb
    cost_perhab = Column(Float) #cost per habitante that would be invested if infra is repared
    falla = Column(Float) # de infraestructura hidráulica por conexiones clandestinas, obstrucción por basura y procesos biofísicos
    falta = Column(Float)
    mantenimiento = Column(Float) # what is the probability this patch is under maitnance
    P_failure = Column(Float)                    #probabilidad de falla
    hundimientos = Column(Float)
    presion_hidraulica = Column(Float) #or an index of low volume of water in the pipes (tandeo)
    poblacion = Column(Integer) # Population size ageb
    uso_suelo = Column(Float)
    urban_growth = Column(Float) # Population growth
    income_index = Column(Float) # Actual income
    presion_social = Column(Float) #social pressure index per ageb (e.g. %pop. involved in the protests?)
    flooding = Column(Float) # mean number of encharcamientos during between 2004 and 2014
    days_wno_water = Column(Integer) # Days with no water

    #Charactersitics of the agebs that define criteria
    houses_with_dranage = Column(Float) # % of houses connected to the dranage from ENEGI survey instrument
    houses_with_abastecimiento = Column(Float) # % houses connected to distribution network
    disease_burden = Column(Integer) # Number of gastrointestinal cases per ageb (from disease model)
    water_quality = Column(Float) # Perception fo water quality
    garbage = Column(Float) # Garbage as the perception of the cause behind obstruction of dranages
    water_needed = Column(Float) # Total water needed based on population size of colonia and water requirements per peson
    water_in = Column(Float) # Water that enters to the colonias
    water_distributed_pipes = Column(Float) # Water imported (not produced in) to the colonia
    water_distributed_trucks = Column(Float) # Water imported (not produced in) to the colonia
    tandeo = Column(Integer) # Hours a week without water?
    scarcity = Column(Float) # When water_needed >  water_produced, deficit > 0
    surplus = Column(Float) # When water_needed <  water_produced, surplus > 0
    eficacia_servicio = Column(Float) #Gestión del servicio de Drenaje y agua potable (ej. interferencia política, no llega la pipa, horario del tandeo, etc)
    desperdicio_agua = Column(Float) #Por fugas, falta de conciencia del uso del agua
    desviacion_agua = Column(Float) #Se llevan el agua a otros lugares
    capacidad = Column(Float) #La Capacidad de la infraestructura hidráulica
    infiltracion = Column(Float)
    rainfall = Column(Float)
    R_tau = Column(Float) #threshold of rainfall acording to protocol
    altura = Column(Float)
    H_f = Column(Float) # undesire state flood
    H_s = Column(Float) #undesire state no water


    #residents decisions metrics
    d_compra_agua = Column(Float) #distance from ideal point for Compra_agua (buying water)
    d_captacion_agua = Column(Float) #distance from ideal point for Captacion_agua (buying tinaco, ranfall storage)
    d_movilizaciones = Column(Float) #distance from ideal point for Movilizaciones
    d_modificacion_vivienda = Column(Float) #distance from ideal point for Modificacion_vivienda
    d_accion_colectiva = Column(Float) #distance from ideal point for Accion_colectiva

    #SACMEX decition metrics
    d_water_extraction = Column(Float)
    d_reparation = Column(Float) #distance from ideal point for decision to repare infrastructure
    d_new = Column(Float) #distance from ideal point for decision to create new infrastructure
    d_water_distribution = Column(Float) #distance from ideal point for decision to distribute water
    d_water_importacion = Column(Float) 

    def __repr__(self):
        return "AGEB%s" % (self.id)


    def protest(self):
        """updates presion_social"""
        if self.d_movilizaciones > random.random():
            delta = 1
        else:
            delta = 0
            
        self.presion_social = 0.9 * self.presion_social + delta
        session.commit()

        
        # def boring(self):
    #     """same sex groups are boring"""
    #     sexes = set([g.sex for g in self.guests])
    #     return len(sexes)==1        

    # def __repr__(self):
    #     mood = "boring" if self.boring() else "exciting"
    #     return "group%s, %s" % (self.id, mood)
    



class Pozo(Base):
    __tablename__ = 'pozos'

    # relationships
    ageb_id = Column(Integer, ForeignKey('agebs.id'))
    ageb = relationship("AGEB", back_populates="pozos")
    
    
    id = Column(Integer, primary_key=True)
    name = Column(String) 
    col_ID = Column(Integer)           #location of well in neighborhood

    Production = Column(Float)       #water production [ m3/day]
    extraction_rate = Column(Float)  #total extraction (defined by zones 1 to 32)
    age_pozo = Column(Integer)         #age of well
    p_failure = Column(Float)       #probability of infrastructure failure here 1 if not infra here
    Ha = Column(Boolean)               #1 if the well is working 0 otherwise

    def __repr__(self):
        return "pozo%s@%s" % (self.id, self.ageb)



