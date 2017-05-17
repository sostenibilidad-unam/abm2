import model
import argparse
import random

model.db.flushdb()

# crear sacmex
s = model.SACMEX(pk=1,
                 status='pause',
                 t=0)

# crear 2400 agebs
for k in range(1,2433):
    d_infra = random.uniform(0.3, 0.6)
    a = model.AGEB(pk=k, d_infra=d_infra, protestant=False, t=0)
