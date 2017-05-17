import model
import argparse
from time import sleep


parser = argparse.ArgumentParser(description='Setup simulation.')
parser.add_argument('--ids', type=int, nargs="+", required=True)
parser.add_argument('--sleep', type=float, default=0.3)
args = parser.parse_args()

while True:
    print [model.AGEB(pk=k) for k in args.ids]
    sleep(args.sleep)
