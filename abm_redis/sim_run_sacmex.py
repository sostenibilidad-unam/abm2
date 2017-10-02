import model
import argparse
import random
from time import sleep

parser = argparse.ArgumentParser(description='Setup simulation.')
parser.add_argument('--sleep', type=float, default=0.2)
args = parser.parse_args()

s = model.SACMEX(pk=1)
s.status = 'play'

print "status set to play"

# as time goes by
while True:
    try:
        s.repara_infras()
        s.t += 1
        print s.t
        while s.count_outdated() > 0:
            sleep(args.sleep)

    except KeyboardInterrupt:
        s.status = 'stop'
        print "status set to stop"
        exit(0)

