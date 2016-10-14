import argparse
import random
import os

parser = argparse.ArgumentParser(description='Create meta-simulation package at workdir')
parser.add_argument('--netlogo', required=True, help='absolute path to netlogo directory')
parser.add_argument('--workdir', required=True, help='absolute path to working directory where meta-simulation will be setup.')
parser.add_argument('--argumentspace', type=argparse.FileType('r'), required=True,
                    help="argument space CSV file")
parser.add_argument('--landscape', default="many-hills",
                    help="type of landscape")
parser.add_argument('--new_infra_investment', type=int, nargs="+")
parser.add_argument('--maintenance', type=int, nargs="+")
parser.add_argument('--budget_distribution', default="competitionbetweenactions")
parser.add_argument('--threads', type=int, default=12)
args = parser.parse_args()



# create working directory
if not os.path.isdir(args.workdir):
    os.makedirs(args.workdir)

# create symlinks to netlogo and extensions
netlogo_jar = os.path.join( args.netlogo, "app/NetLogo.jar")
netlogo_csv = os.path.join( args.netlogo, "app/extensions/csv")
netlogo_matrix = os.path.join( args.netlogo, "app/extensions/matrix")

assert os.path.exists(netlogo_jar)
assert os.path.exists(netlogo_csv)
assert os.path.exists(netlogo_matrix)

os.symlink(netlogo_jar, os.path.join(args.workdir, "NetLogo.jar"))
os.symlink(netlogo_csv, os.path.join(args.workdir, "csv"))
os.symlink(netlogo_matrix, os.path.join(args.workdir, "matrix"))

# create symlinks to model, argumentspace and run script
this_dir = os.path.dirname(os.path.realpath(__file__))
os.symlink(os.path.join(this_dir, "ABM_V2.0.nlogo"), os.path.join(args.workdir, "ABM_V2.0.nlogo"))
os.symlink(os.path.join(this_dir, args.argumentspace.name), os.path.join(args.workdir, args.argumentspace.name))
os.symlink(os.path.join(this_dir, "run.sh"), os.path.join(args.workdir, "run.sh"))

# read setup and submit templates
setup_template = open('setup_template.xml').read()
condor_template= open('submit_template.condor').read()

lines = args.argumentspace.readlines()

# create setup XML files and condor files
for simulation_number in range(len(lines)-1):
    for new_infra_investment in args.new_infra_investment:
        for maintenance in args.maintenance:
            random_seed = random.randint(0, 100000)
            run_id = "nii%s_mii%s_%s_%s" % (new_infra_investment,
                                            maintenance,
                                            args.landscape,
                                            simulation_number)
            with open('%s/setup_%s.xml' % (args.workdir, run_id), 'w') as setupfile, \
                 open('%s/submit_%s.condor' % (args.workdir, run_id), 'w') as condorfile:
                setupfile.write(setup_template.format(simulation_number=simulation_number,
                                                      new_infra_investment=new_infra_investment,
                                                      maintenance=maintenance,
                                                      landscape=args.landscape,
                                                      budget_distribution=args.budget_distribution,
                                                      random_seed=random_seed,
                                                      threads=args.threads))
                condorfile.write(condor_template.format(run_id=run_id,
                                                        threads=args.threads))
