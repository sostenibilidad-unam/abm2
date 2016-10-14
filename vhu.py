import argparse
import random

parser = argparse.ArgumentParser(description='Create simulation setup file')
parser.add_argument('--argumentspace', type=argparse.FileType('r'), required=True,
                    help="argument space CSV file")
parser.add_argument('--landscape', default="many-hills",
                    help="type of landscape")
parser.add_argument('--new_infra_investment', type=int, nargs="+")
parser.add_argument('--maintenance', type=int, nargs="+")
parser.add_argument('--budget_distribution', default="competitionbetweenactions")
parser.add_argument('--threads', type=int, default=12)
args = parser.parse_args()


lines = args.argumentspace.readlines()

# TODO: use jinja or something
setup_template = open('../setup_template.xml').read()
# TODO: create condor template
condor_template= open('../submit_template.condor').read()

# TODO: maybe simlink extensions?

# create setup XML files and condor files
for simulation_number in range(len(lines)-1):
    for new_infra_investment in args.new_infra_investment:
        for maintenance in args.maintenance:
            random_seed = random.randint(100000)
            run_id = "nii%s_mii%s_%s_%s" % (new_infra_investment,
                                            maintenance,
                                            args.landscape,
                                            simulation_number)
            with open('setup_%s.xml' % run_id, 'w') as setupfile, \
                 open('submit_%s.condor' % run_id, 'w') as condorfile:
                setupfile.write(setup_template.format(simulation_number=simulation_number,
                                                      new_infra_investment=new_infra_investment,
                                                      maintenance=maintenance,
                                                      landscape=args.landscape,
                                                      budget_distribution=budget_distribution,
                                                      random_seed=random_seed,
                                                      threads=args.threads))
                condorfile.write(condor_template.format(run_id=run_id,
                                                        threads=args.threads))
