import model
from value_functions import lineal


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



class ReparaInfra:

    def __init__(self, limit_matrix, context, ageb):
        self.limit_matrix = limit_matrix
        self.context = context
        self.ageb = ageb

    def get_edad_infra(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_capacidad(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_falla(self):
        return lineal(self.ageb.fallain,
                      self.context['fallain']['min'],
                      self.context['fallain']['max'])


    def get_falta(self):
        return lineal(self.ageb.faltain,
                      self.context['falta_infraestructura']['min'],
                      self.context['falta_infraestructura']['max'])


    def get_presion_hidraulica(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_monto(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_calidad_agua(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_escasez_agua(self):
        return lineal(self.ageb.escasez,
                      self.context['escasez_agua']['min'],
                      self.context['escasez_agua']['max'])


    def get_inundaciones(self):
        return lineal(self.ageb.total_ench,
                      self.context['inundaciones']['min'],
                      self.context['inundaciones']['max'])


    def get_abastecimiento(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_peticion_delegaciones(self):
        return lineal(self.ageb.petdels,
                      self.context['peticion_delegaciones']['min'],
                      self.context['peticion_delegaciones']['max'])


    def get_presion_medios(self):
        return lineal(self.ageb.presmed,
                      self.context['presion_medios']['min'],
                      self.context['presion_medios']['max'])


    def get_presion_social(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_distance(self):
        return ideal_distance(alpha=self.limit_matrix.alternatives['repara_infra'],
                              criteria_weights=self.limit_matrix.criteria.values(),
                              criteria=[
                                  self.get_edad_infra(),
                                  self.get_capacidad(),
                                  self.get_falla(),
                                  self.get_falta(),
                                  self.get_presion_hidraulica(),
                                  self.get_monto(),
                                  self.get_calidad_agua(),
                                  self.get_escasez_agua(),
                                  self.get_inundaciones(),
                                  self.get_abastecimiento(),
                                  self.get_peticion_delegaciones(),
                                  self.get_presion_medios(),
                                  self.get_presion_social(),
                                  ],
                              exponent=2)



class DistribucionAgua:

    def __init__(self, limit_matrix, context, ageb):
        self.limit_matrix = limit_matrix
        self.context = context
        self.ageb = ageb

    def get_edad_infra(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_capacidad(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_falla(self):
        return lineal(self.ageb.fallain,
                      self.context['fallain']['min'],
                      self.context['fallain']['max'])


    def get_falta(self):
        return lineal(self.ageb.faltain,
                      self.context['falta_infraestructura']['min'],
                      self.context['falta_infraestructura']['max'])


    def get_presion_hidraulica(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_monto(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_calidad_agua(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_escasez_agua(self):
        return lineal(self.ageb.escasez,
                      self.context['escasez_agua']['min'],
                      self.context['escasez_agua']['max'])


    def get_inundaciones(self):
        return lineal(self.ageb.total_ench,
                      self.context['inundaciones']['min'],
                      self.context['inundaciones']['max'])


    def get_abastecimiento(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_peticion_delegaciones(self):
        return lineal(self.ageb.petdels,
                      self.context['peticion_delegaciones']['min'],
                      self.context['peticion_delegaciones']['max'])


    def get_presion_medios(self):
        return lineal(self.ageb.presmed,
                      self.context['presion_medios']['min'],
                      self.context['presion_medios']['max'])


    def get_presion_social(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_distance(self):
        return ideal_distance(alpha=self.limit_matrix.alternatives['distribucion_agua'],
                              criteria_weights=self.limit_matrix.criteria.values(),
                              criteria=[
                                  self.get_edad_infra(),
                                  self.get_capacidad(),
                                  self.get_falla(),
                                  self.get_falta(),
                                  self.get_presion_hidraulica(),
                                  self.get_monto(),
                                  self.get_calidad_agua(),
                                  self.get_escasez_agua(),
                                  self.get_inundaciones(),
                                  self.get_abastecimiento(),
                                  self.get_peticion_delegaciones(),
                                  self.get_presion_medios(),
                                  self.get_presion_social(),
                                  ],
                              exponent=2)



class ExtraccionAgua:

    def __init__(self, limit_matrix, context, ageb):
        self.limit_matrix = limit_matrix
        self.context = context
        self.ageb = ageb

    def get_edad_infra(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_capacidad(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_falla(self):
        return lineal(self.ageb.fallain,
                      self.context['fallain']['min'],
                      self.context['fallain']['max'])


    def get_falta(self):
        return lineal(self.ageb.faltain,
                      self.context['falta_infraestructura']['min'],
                      self.context['falta_infraestructura']['max'])


    def get_presion_hidraulica(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_monto(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_calidad_agua(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_escasez_agua(self):
        return lineal(self.ageb.escasez,
                      self.context['escasez_agua']['min'],
                      self.context['escasez_agua']['max'])


    def get_inundaciones(self):
        return lineal(self.ageb.total_ench,
                      self.context['inundaciones']['min'],
                      self.context['inundaciones']['max'])


    def get_abastecimiento(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_peticion_delegaciones(self):
        return lineal(self.ageb.petdels,
                      self.context['peticion_delegaciones']['min'],
                      self.context['peticion_delegaciones']['max'])


    def get_presion_medios(self):
        return lineal(self.ageb.presmed,
                      self.context['presion_medios']['min'],
                      self.context['presion_medios']['max'])


    def get_presion_social(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_distance(self):
        return ideal_distance(alpha=self.limit_matrix.alternatives['extraccion_agua'],
                              criteria_weights=self.limit_matrix.criteria.values(),
                              criteria=[
                                  self.get_edad_infra(),
                                  self.get_capacidad(),
                                  self.get_falla(),
                                  self.get_falta(),
                                  self.get_presion_hidraulica(),
                                  self.get_monto(),
                                  self.get_calidad_agua(),
                                  self.get_escasez_agua(),
                                  self.get_inundaciones(),
                                  self.get_abastecimiento(),
                                  self.get_peticion_delegaciones(),
                                  self.get_presion_medios(),
                                  self.get_presion_social(),
                                  ],
                              exponent=2)



class ImportacionAgua:

    def __init__(self, limit_matrix, context, ageb):
        self.limit_matrix = limit_matrix
        self.context = context
        self.ageb = ageb

    def get_edad_infra(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_capacidad(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_falla(self):
        return lineal(self.ageb.fallain,
                      self.context['fallain']['min'],
                      self.context['fallain']['max'])


    def get_falta(self):
        return lineal(self.ageb.faltain,
                      self.context['falta_infraestructura']['min'],
                      self.context['falta_infraestructura']['max'])


    def get_presion_hidraulica(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_monto(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_calidad_agua(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_escasez_agua(self):
        return lineal(self.ageb.escasez,
                      self.context['escasez_agua']['min'],
                      self.context['escasez_agua']['max'])


    def get_inundaciones(self):
        return lineal(self.ageb.total_ench,
                      self.context['inundaciones']['min'],
                      self.context['inundaciones']['max'])


    def get_abastecimiento(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_peticion_delegaciones(self):
        return lineal(self.ageb.petdels,
                      self.context['peticion_delegaciones']['min'],
                      self.context['peticion_delegaciones']['max'])


    def get_presion_medios(self):
        return lineal(self.ageb.presmed,
                      self.context['presion_medios']['min'],
                      self.context['presion_medios']['max'])


    def get_presion_social(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_distance(self):
        return ideal_distance(alpha=self.limit_matrix.alternatives['importacion_agua'],
                              criteria_weights=self.limit_matrix.criteria.values(),
                              criteria=[
                                  self.get_edad_infra(),
                                  self.get_capacidad(),
                                  self.get_falla(),
                                  self.get_falta(),
                                  self.get_presion_hidraulica(),
                                  self.get_monto(),
                                  self.get_calidad_agua(),
                                  self.get_escasez_agua(),
                                  self.get_inundaciones(),
                                  self.get_abastecimiento(),
                                  self.get_peticion_delegaciones(),
                                  self.get_presion_medios(),
                                  self.get_presion_social(),
                                  ],
                              exponent=2)



class Mantenimiento:

    def __init__(self, limit_matrix, context, ageb):
        self.limit_matrix = limit_matrix
        self.context = context
        self.ageb = ageb

    def get_edad_infra(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_capacidad(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_falla(self):
        return lineal(self.ageb.fallain,
                      self.context['fallain']['min'],
                      self.context['fallain']['max'])


    def get_falta(self):
        return lineal(self.ageb.faltain,
                      self.context['falta_infraestructura']['min'],
                      self.context['falta_infraestructura']['max'])


    def get_presion_hidraulica(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_monto(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_calidad_agua(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_escasez_agua(self):
        return lineal(self.ageb.escasez,
                      self.context['escasez_agua']['min'],
                      self.context['escasez_agua']['max'])


    def get_inundaciones(self):
        return lineal(self.ageb.total_ench,
                      self.context['inundaciones']['min'],
                      self.context['inundaciones']['max'])


    def get_abastecimiento(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_peticion_delegaciones(self):
        return lineal(self.ageb.petdels,
                      self.context['peticion_delegaciones']['min'],
                      self.context['peticion_delegaciones']['max'])


    def get_presion_medios(self):
        return lineal(self.ageb.presmed,
                      self.context['presion_medios']['min'],
                      self.context['presion_medios']['max'])


    def get_presion_social(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_distance(self):
        return ideal_distance(alpha=self.limit_matrix.alternatives['mantenimiento'],
                              criteria_weights=self.limit_matrix.criteria.values(),
                              criteria=[
                                  self.get_edad_infra(),
                                  self.get_capacidad(),
                                  self.get_falla(),
                                  self.get_falta(),
                                  self.get_presion_hidraulica(),
                                  self.get_monto(),
                                  self.get_calidad_agua(),
                                  self.get_escasez_agua(),
                                  self.get_inundaciones(),
                                  self.get_abastecimiento(),
                                  self.get_peticion_delegaciones(),
                                  self.get_presion_medios(),
                                  self.get_presion_social(),
                                  ],
                              exponent=2)



class NuevaInfraestructura:

    def __init__(self, limit_matrix, context, ageb):
        self.limit_matrix = limit_matrix
        self.context = context
        self.ageb = ageb

    def get_edad_infra(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_capacidad(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_falla(self):
        return lineal(self.ageb.fallain,
                      self.context['fallain']['min'],
                      self.context['fallain']['max'])


    def get_falta(self):
        return lineal(self.ageb.faltain,
                      self.context['falta_infraestructura']['min'],
                      self.context['falta_infraestructura']['max'])


    def get_presion_hidraulica(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_monto(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_calidad_agua(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_escasez_agua(self):
        return lineal(self.ageb.escasez,
                      self.context['escasez_agua']['min'],
                      self.context['escasez_agua']['max'])


    def get_inundaciones(self):
        return lineal(self.ageb.total_ench,
                      self.context['inundaciones']['min'],
                      self.context['inundaciones']['max'])


    def get_abastecimiento(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_peticion_delegaciones(self):
        return lineal(self.ageb.petdels,
                      self.context['peticion_delegaciones']['min'],
                      self.context['peticion_delegaciones']['max'])


    def get_presion_medios(self):
        return lineal(self.ageb.presmed,
                      self.context['presion_medios']['min'],
                      self.context['presion_medios']['max'])


    def get_presion_social(self):
        return lineal(self.ageb.edad_infra,
                      self.context['edad_infra']['min'],
                      self.context['edad_infra']['max'])


    def get_distance(self):
        return ideal_distance(alpha=self.limit_matrix.alternatives['nueva_infraestructura'],
                              criteria_weights=self.limit_matrix.criteria.values(),
                              criteria=[
                                  self.get_edad_infra(),
                                  self.get_capacidad(),
                                  self.get_falla(),
                                  self.get_falta(),
                                  self.get_presion_hidraulica(),
                                  self.get_monto(),
                                  self.get_calidad_agua(),
                                  self.get_escasez_agua(),
                                  self.get_inundaciones(),
                                  self.get_abastecimiento(),
                                  self.get_peticion_delegaciones(),
                                  self.get_presion_medios(),
                                  self.get_presion_social(),
                                  ],
                              exponent=2)

