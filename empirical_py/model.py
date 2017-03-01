# coding: utf-8

from sqlalchemy import Column, Integer, ForeignKey, Float, Boolean, String
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.ext.declarative import declarative_base
import random
import pandas as pd

Base = declarative_base()

class AGEB(Base):

    def __init__(self, SacmexMatrixPath, residentMatrixPath=None):
        self.SACMEX_Matrix = LimitMatrix(SacmexMatrixPath)
        
    
    __tablename__ = 'agebs'
    id = Column(Integer, primary_key=True)

    # relationships
    pozos = relationship("Pozo", back_populates="ageb")
    
    #paches_set_agebs = Column() #the set of patches that bellow to the ageb
        
    # attributes
    group_kmean = Column(Integer) # define to witch group an ageb belongs to, based on sosio-economic charactersitics
    zona_aquifera = Column(Integer)
    name_delegation = Column(String) #the name of the delegation the ageb belongs to

    monto = Column(Float) # resources designated to each ageb (delegations?)

    def update_monto(self):
        self.monto = asdlkfjas;dlk
    
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

    
    def update_d_reparation(self, c1_max, value_function):
        #calcular las las tres listas c1 c1_max y V
        # y con eso distance_ideal para definir el valor de d_reparacion
        
        wf  = [0.0625, 0.125, 0.2,5 0.5, 1]
        wfi = [1, 0.5, 0.25, 0.125, 0.0625]
        
        V = [
            value_function(self.antiguedad_infra,   [0.1, 0.3, 0.7, 0.9], ["", "", "", ""], c1_max[0], wf),
            value_function(self.capacidad,          [0.1, 0.3, 0.7, 0.9], ["", "", "", ""], c1_max[1], wfi),
            value_function(self.falla,              [0.1, 0.3, 0.7, 0.9], ["", "", "", ""], c1_max[2], wf),
            value_function(self.falta,           [0.9, 0.95, 0.97, 0.99], ["", "", "", ""], c1_max[3], wf),
            value_function(self.presion_hidraulica, [0.1, 0.3, 0.7, 0.9], ["", "", "", ""], c1_max[4], wfi),
            value_function(self.monto,              [0.1, 0.3, 0.7, 0.9], ["", "", "", ""], c1_max[5], wf),
            value_function(self.water_quality,      [0.1, 0.3, 0.7, 0.9], ["", "", "", ""], c1_max[6], wfi),
            value_function(self.scarcity,           [0.1, 0.3, 0.7, 0.9], ["", "", "", ""], c1_max[7], wf),
            value_function(self.flooding,           [0.1, 0.4, 0.6, 0.8], ["", "", "", ""], c1_max[8], wf),
            value_function(self.abastecimiento,     [0.1, 0.3, 0.7, 0.9], ["", "", "", ""], c1_max[9], wf),
            value_function(1,                       [0.1, 0.3, 0.7, 0.9], ["", "", "", ""], c1_max[10], wf), # petición de delegaciones
            value_function(presion_de_medios,       [0.1, 0.3, 0.7, 0.9], ["", "", "", ""], c1_max[11], wf),
            value_function(self.presion_social,     [0.1, 0.3, 0.7, 0.9], ["", "", "", ""], c1_max[12], wf)]
        
        self.d_reparation = ideal_distance(self.SACMEX_Matrix.w_limit,
                                           V,
                                           self.SACMEX_Matrix.weighted_criteria,
                                           2)
    

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


class SACMEX:
    recursos_para_mantencion = 40

    def update_c1_max(self):
       

        self.c1_max = [ session.query(AGEB).order_by(AGEB.antiguedad_infra.desc()).first().antiguedad_infra,
                        session.query(AGEB).order_by(AGEB.capacidad.desc()).first().capacidad,
                        session.query(AGEB).order_by(AGEB.falla.desc()).first().falla,
                        session.query(AGEB).order_by(AGEB.falta.desc()).first().falta,
                        session.query(AGEB).order_by(AGEB.presion_hidraulica.desc()).first().presion_hidraulica,
                        session.query(AGEB).order_by(AGEB.monto.desc()).first().monto,
                        session.query(AGEB).order_by(AGEB.water_quality.desc()).first().water_quality,
                        session.query(AGEB).order_by(AGEB.scarcity.desc()).first().scarcity,
                        session.query(AGEB).order_by(AGEB.flooding.desc()).first().flooding,
                        session.query(AGEB).order_by(AGEB.abastecimiento.desc()).first().abastecimiento,
                        1,
                        session.query(AGEB).order_by(AGEB.presion_de_medios.desc()).first().presion_de_medios,
                        session.query(AGEB).order_by(AGEB.presion_social.desc()).first().presion_social
                    ]
        

    # def decide(self):
    #     for a in session.query(AGEB).all():
    #         a.update_d_rep(self.c1_max, value_function)
            
    
    def reparar_infra(self):
        budget = 0
        for ageb in session.query(AGEB).order_by(AGEB.d_reparation): # es decendiente?
            if budget < self.recursos_para_mantencion:
                ageb.antiguedad_infra = 0.8 * ageb.antiguedad_infra
                budget += 1
                session.commit()






    
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





class LimitMatrix:
    def __init__(self, csv_path):
        df = pd.read_csv(csv_path, encoding="latin1")
        firstCriteriaRow = [i for i, x in enumerate(df.ix[:,0]) if "nan" not in str(x)][1]  #the index of the second non null cell in first column
        self.alternative_names = df.ix[1:firstCriteriaRow-1,1]
        self.criteria_names = df.ix[firstCriteriaRow:,1]
        w_sum = sum(pd.to_numeric(df.ix[firstCriteriaRow:,2]))
        
        self.weighted_criteria = pd.to_numeric(df.ix[firstCriteriaRow:,2]).apply(lambda x:x/w_sum)

        self.w_limit = df[5,2] / sum(pd.to_numeric(df.ix[2:6,2]))    #esto talvez deberia ser una lista (un valor para cada alternativa), por ahora el 5 es para la alternativa mantenimiento

        



def ideal_distance(alpha, VF_list, weight_list, h_Cp):
    """
    this function calcualtes a distance to ideal point using compromized programing metric
    arguments:
    - VF_list: a list of value functions
    - weight_list a list of weights from the alternatives criteria links (CA_links)
    - h_Cp to control the type of distance h_Cp=2 euclidian; h_Cp=1 manhattan
    """
    return alpha * sum([weight_list[n]**h_Cp * VF_list[n]**h_Cp for n in range(len(weight_list))])**(1/h_Cp)

   
def value_function(A, B, C, D, EE):
    """
    This function reports a standarized value for the relationship between value of criteria and motivation to acta
    A the value of a biophysical variable in its natural scale
    B a list of percentage values of the biofisical variable that reflexts on the cut-offs to define the limits of the range in the linguistic scale
    C list of streengs that define the lisguistice scale associate with a viobisical variable
    D the ideal or anti ideal point of the criteria define based on the linguistic scale (e.g. intolerable ~= anti-ideal)
    EE a list of standard values to map the natural scales
  """
    if A > B[3] * D:
        SM = EE[4]
    if A > B[2] * D and  A <= B[3] * D:
        SM = EE[3]
    if A > B[1] * D and  A <= B[2] * D:
        SM = E[2]
    if A > B[0] * D and  A <= B[1] * D:
        SM = E[1]
    if A <= B[0] * D:
        SM = E[0]
    return SM

 
