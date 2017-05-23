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


class AccionColectiva:
    def __init__(self, limit_matrix, context, ageb):
        self.limit_matrix = limit_matrix
        self.context = context
        self.ageb = ageb

    def get_contaminacion_agua(self):
        return lineal(self.ageb.escasez,
                      self.context['contaminacion_agua']['min'],
                      self.context['contaminacion_agua']['max'])

    def get_crecimiento_urbano(self):
        return lineal(self.ageb.escasez,
                      self.context['crecimiento_urbano']['min'],
                      self.context['crecimiento_urbano']['max'])
        

    def get_desperdicio_agua(self):
        return lineal(self.ageb.escasez,
                      self.context['desperdicio_agua']['min'],
                      self.context['desperdicio_agua']['max'])

    def get_desviacion_agua(self):
        return lineal(self.ageb.escasez,
                      self.context['desviacion_agua']['min'],
                      self.context['desviacion_agua']['max'])

    def get_eficacia_servicio(self):
        return lineal(self.ageb.escasez,
                      self.context['eficacia_servicio']['min'],
                      self.context['eficacia_servicio']['max'])

    def get_falta_infraestructura(self):
        return lineal(self.ageb.escasez,
                      self.context['falta_infraestructura']['min'],
                      self.context['falta_infraestructura']['max'])

    def get_obstruccion_alcantarillado(self):
        return lineal(self.ageb.escasez,
                      self.context['obstruccion_alcantarillado']['min'],
                      self.context['obstruccion_alcantarillado']['max'])

    def get_escasez_agua(self):
        return lineal(self.ageb.escasez,
                      self.context['escasez_agua']['min'],
                      self.context['escasez_agua']['max'])

    def get_inundaciones(self):
        return lineal(self.ageb.escasez,
                      self.context['inundaciones']['min'],
                      self.context['inundaciones']['max'])

    def get_salud(self):
        return lineal(self.ageb.escasez,
                      self.context['salud']['min'],
                      self.context['salud']['max'])


    def get_distance(self):
        return ideal_distance(alpha=self.limit_matrix.alternatives['accion_colectiva'],
                              criteria_weights=self.limit_matrix.criteria.values(),
                              criteria=[
                                  self.get_contaminacion_agua(),
                                  self.get_crecimiento_urbano(),
                                  self.get_desperdicio_agua(),
                                  self.get_desviacion_agua(),
                                  self.get_eficacia_servicio(),
                                  self.get_falta_infraestructura(),
                                  self.get_obstruccion_alcantarillado(),
                                  self.get_escasez_agua(),
                                  self.get_inundaciones(),
                                  self.get_salud(),
                                  ],
                              exponent=2)


class CaptacionAgua:
    def __init__(self, limit_matrix, context, ageb):
        self.limit_matrix = limit_matrix
        self.context = context
        self.ageb = ageb

    def get_contaminacion_agua(self):
        return lineal(self.ageb.escasez,
                      self.context['contaminacion_agua']['min'],
                      self.context['contaminacion_agua']['max'])

    def get_crecimiento_urbano(self):
        return lineal(self.ageb.escasez,
                      self.context['crecimiento_urbano']['min'],
                      self.context['crecimiento_urbano']['max'])
        

    def get_desperdicio_agua(self):
        return lineal(self.ageb.escasez,
                      self.context['desperdicio_agua']['min'],
                      self.context['desperdicio_agua']['max'])

    def get_desviacion_agua(self):
        return lineal(self.ageb.escasez,
                      self.context['desviacion_agua']['min'],
                      self.context['desviacion_agua']['max'])

    def get_eficacia_servicio(self):
        return lineal(self.ageb.escasez,
                      self.context['eficacia_servicio']['min'],
                      self.context['eficacia_servicio']['max'])

    def get_falta_infraestructura(self):
        return lineal(self.ageb.escasez,
                      self.context['falta_infraestructura']['min'],
                      self.context['falta_infraestructura']['max'])

    def get_obstruccion_alcantarillado(self):
        return lineal(self.ageb.escasez,
                      self.context['obstruccion_alcantarillado']['min'],
                      self.context['obstruccion_alcantarillado']['max'])

    def get_escasez_agua(self):
        return lineal(self.ageb.escasez,
                      self.context['escasez_agua']['min'],
                      self.context['escasez_agua']['max'])

    def get_inundaciones(self):
        return lineal(self.ageb.escasez,
                      self.context['inundaciones']['min'],
                      self.context['inundaciones']['max'])

    def get_salud(self):
        return lineal(self.ageb.escasez,
                      self.context['salud']['min'],
                      self.context['salud']['max'])


    def get_distance(self):
        return ideal_distance(alpha=self.limit_matrix.alternatives['captacion_de_agua'],
                              criteria_weights=self.limit_matrix.criteria.values(),
                              criteria=[
                                  self.get_contaminacion_agua(),
                                  self.get_crecimiento_urbano(),
                                  self.get_desperdicio_agua(),
                                  self.get_desviacion_agua(),
                                  self.get_eficacia_servicio(),
                                  self.get_falta_infraestructura(),
                                  self.get_obstruccion_alcantarillado(),
                                  self.get_escasez_agua(),
                                  self.get_inundaciones(),
                                  self.get_salud(),
                                  ],
                              exponent=2)


class CompraAgua:
    def __init__(self, limit_matrix, context, ageb):
        self.limit_matrix = limit_matrix
        self.context = context
        self.ageb = ageb

    def get_contaminacion_agua(self):
        return lineal(self.ageb.escasez,
                      self.context['contaminacion_agua']['min'],
                      self.context['contaminacion_agua']['max'])

    def get_crecimiento_urbano(self):
        return lineal(self.ageb.escasez,
                      self.context['crecimiento_urbano']['min'],
                      self.context['crecimiento_urbano']['max'])
        

    def get_desperdicio_agua(self):
        return lineal(self.ageb.escasez,
                      self.context['desperdicio_agua']['min'],
                      self.context['desperdicio_agua']['max'])

    def get_desviacion_agua(self):
        return lineal(self.ageb.escasez,
                      self.context['desviacion_agua']['min'],
                      self.context['desviacion_agua']['max'])

    def get_eficacia_servicio(self):
        return lineal(self.ageb.escasez,
                      self.context['eficacia_servicio']['min'],
                      self.context['eficacia_servicio']['max'])

    def get_falta_infraestructura(self):
        return lineal(self.ageb.escasez,
                      self.context['falta_infraestructura']['min'],
                      self.context['falta_infraestructura']['max'])

    def get_obstruccion_alcantarillado(self):
        return lineal(self.ageb.escasez,
                      self.context['obstruccion_alcantarillado']['min'],
                      self.context['obstruccion_alcantarillado']['max'])

    def get_escasez_agua(self):
        return lineal(self.ageb.escasez,
                      self.context['escasez_agua']['min'],
                      self.context['escasez_agua']['max'])

    def get_inundaciones(self):
        return lineal(self.ageb.escasez,
                      self.context['inundaciones']['min'],
                      self.context['inundaciones']['max'])

    def get_salud(self):
        return lineal(self.ageb.escasez,
                      self.context['salud']['min'],
                      self.context['salud']['max'])


    def get_distance(self):
        return ideal_distance(alpha=self.limit_matrix.alternatives['compra_de_agua'],
                              criteria_weights=self.limit_matrix.criteria.values(),
                              criteria=[
                                  self.get_contaminacion_agua(),
                                  self.get_crecimiento_urbano(),
                                  self.get_desperdicio_agua(),
                                  self.get_desviacion_agua(),
                                  self.get_eficacia_servicio(),
                                  self.get_falta_infraestructura(),
                                  self.get_obstruccion_alcantarillado(),
                                  self.get_escasez_agua(),
                                  self.get_inundaciones(),
                                  self.get_salud(),
                                  ],
                              exponent=2)

class ModificacionVivienda:
    def __init__(self, limit_matrix, context, ageb):
        self.limit_matrix = limit_matrix
        self.context = context
        self.ageb = ageb

    def get_contaminacion_agua(self):
        return lineal(self.ageb.escasez,
                      self.context['contaminacion_agua']['min'],
                      self.context['contaminacion_agua']['max'])

    def get_crecimiento_urbano(self):
        return lineal(self.ageb.escasez,
                      self.context['crecimiento_urbano']['min'],
                      self.context['crecimiento_urbano']['max'])
        

    def get_desperdicio_agua(self):
        return lineal(self.ageb.escasez,
                      self.context['desperdicio_agua']['min'],
                      self.context['desperdicio_agua']['max'])

    def get_desviacion_agua(self):
        return lineal(self.ageb.escasez,
                      self.context['desviacion_agua']['min'],
                      self.context['desviacion_agua']['max'])

    def get_eficacia_servicio(self):
        return lineal(self.ageb.escasez,
                      self.context['eficacia_servicio']['min'],
                      self.context['eficacia_servicio']['max'])

    def get_falta_infraestructura(self):
        return lineal(self.ageb.escasez,
                      self.context['falta_infraestructura']['min'],
                      self.context['falta_infraestructura']['max'])

    def get_obstruccion_alcantarillado(self):
        return lineal(self.ageb.escasez,
                      self.context['obstruccion_alcantarillado']['min'],
                      self.context['obstruccion_alcantarillado']['max'])

    def get_escasez_agua(self):
        return lineal(self.ageb.escasez,
                      self.context['escasez_agua']['min'],
                      self.context['escasez_agua']['max'])

    def get_inundaciones(self):
        return lineal(self.ageb.escasez,
                      self.context['inundaciones']['min'],
                      self.context['inundaciones']['max'])

    def get_salud(self):
        return lineal(self.ageb.escasez,
                      self.context['salud']['min'],
                      self.context['salud']['max'])


    def get_distance(self):
        return ideal_distance(alpha=self.limit_matrix.alternatives['modificacion_de_vivienda'],
                              criteria_weights=self.limit_matrix.criteria.values(),
                              criteria=[
                                  self.get_contaminacion_agua(),
                                  self.get_crecimiento_urbano(),
                                  self.get_desperdicio_agua(),
                                  self.get_desviacion_agua(),
                                  self.get_eficacia_servicio(),
                                  self.get_falta_infraestructura(),
                                  self.get_obstruccion_alcantarillado(),
                                  self.get_escasez_agua(),
                                  self.get_inundaciones(),
                                  self.get_salud(),
                                  ],
                              exponent=2)

class Movilizaciones:
    def __init__(self, limit_matrix, context, ageb):
        self.limit_matrix = limit_matrix
        self.context = context
        self.ageb = ageb

    def get_contaminacion_agua(self):
        return lineal(self.ageb.escasez,
                      self.context['contaminacion_agua']['min'],
                      self.context['contaminacion_agua']['max'])

    def get_crecimiento_urbano(self):
        return lineal(self.ageb.escasez,
                      self.context['crecimiento_urbano']['min'],
                      self.context['crecimiento_urbano']['max'])
        

    def get_desperdicio_agua(self):
        return lineal(self.ageb.escasez,
                      self.context['desperdicio_agua']['min'],
                      self.context['desperdicio_agua']['max'])

    def get_desviacion_agua(self):
        return lineal(self.ageb.escasez,
                      self.context['desviacion_agua']['min'],
                      self.context['desviacion_agua']['max'])

    def get_eficacia_servicio(self):
        return lineal(self.ageb.escasez,
                      self.context['eficacia_servicio']['min'],
                      self.context['eficacia_servicio']['max'])

    def get_falta_infraestructura(self):
        return lineal(self.ageb.escasez,
                      self.context['falta_infraestructura']['min'],
                      self.context['falta_infraestructura']['max'])

    def get_obstruccion_alcantarillado(self):
        return lineal(self.ageb.escasez,
                      self.context['obstruccion_alcantarillado']['min'],
                      self.context['obstruccion_alcantarillado']['max'])

    def get_escasez_agua(self):
        return lineal(self.ageb.escasez,
                      self.context['escasez_agua']['min'],
                      self.context['escasez_agua']['max'])

    def get_inundaciones(self):
        return lineal(self.ageb.escasez,
                      self.context['inundaciones']['min'],
                      self.context['inundaciones']['max'])

    def get_salud(self):
        return lineal(self.ageb.escasez,
                      self.context['salud']['min'],
                      self.context['salud']['max'])


    def get_distance(self):
        return ideal_distance(alpha=self.limit_matrix.alternatives['movilizaciones'],
                              criteria_weights=self.limit_matrix.criteria.values(),
                              criteria=[
                                  self.get_contaminacion_agua(),
                                  self.get_crecimiento_urbano(),
                                  self.get_desperdicio_agua(),
                                  self.get_desviacion_agua(),
                                  self.get_eficacia_servicio(),
                                  self.get_falta_infraestructura(),
                                  self.get_obstruccion_alcantarillado(),
                                  self.get_escasez_agua(),
                                  self.get_inundaciones(),
                                  self.get_salud(),
                                  ],
                              exponent=2)
