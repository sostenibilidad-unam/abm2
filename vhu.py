import argparse

parser = argparse.ArgumentParser(description='Create simulation setup file')
parser.add_argument('--simulation', type=int, help="row number from parameter space table", required=True)
parser.add_argument('--landscape', help="type of landscape", default="many-hills")
args = parser.parse_args()

template = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE experiments SYSTEM "behaviorspace.dtd">
<experiments>
  <experiment name="experiment" repetitions="20" runMetricsEveryStep="false">
    <setup>setup</setup>
    <go>go</go>
    <timeLimit steps="300"/>
    <metric>InequalityExposureIndex</metric>
    <metric>ExposureIndex</metric>
    <metric>ExposureIndex_S</metric>
    <metric>ExposureIndex_F</metric>
    <metric>StateinfraIndex_S</metric>
    <metric>StateinfraIndex_F</metric>
    <metric>socialpressureIndex_S</metric>
    <metric>socialpressureIndex_F</metric>
    <metric>StateinfraAgeIndex_S</metric>
    <metric>StateinfraAgeIndex_F</metric>
    <metric>w_11_demanda_F</metric>
    <metric>w_12_presion_F</metric>
    <metric>w_13_estado_F</metric>
    <metric>w_21_necesidad_F</metric>
    <metric>w_22_presion_F</metric>
    <metric>w_23_estado_F</metric>
    <metric>w_31_demanda_S</metric>
    <metric>w_32_presion_S</metric>
    <metric>w_33_estado_S</metric>
    <metric>w_41_necesidad_S</metric>
    <metric>w_42_presion_S</metric>
    <metric>w_43_estado_S</metric>
    <enumeratedValueSet variable="New_infra_investment">
      <value value="100"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="maintenance">
      <value value="130"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="landscape-type">
      <value value="&quot;{landscape}&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Initial-Condition-Infrastructure">
      <value value="&quot;Worse&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="semilla-aleatoria">
      <value value="48569"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="p_rain">
      <value value="0.5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="simulation_number">
      <value value="{simulation_number}"/>
    </enumeratedValueSet>
  </experiment>
</experiments>"""

with open('setup_%s_%s.xml' % (args.landscape, args.simulation), 'w') as setupfile:
    setupfile.write(template.format(simulation_number=args.simulation,
                                    landscape=args.landscape))

