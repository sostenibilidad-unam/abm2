import argparse

parser = argparse.ArgumentParser(description='Create simulation setup file')
parser.add_argument('--argumentspace', type=argparse.FileType('r'), required=True,
                    help="argument space CSV file")
parser.add_argument('--landscape', help="type of landscape", default="many-hills")
parser.add_argument('--new_infra_investment', type=int, nargs="+")
parser.add_argument('--maintenance', type=int, nargs="+")
args = parser.parse_args()


lines = args.argumentspace.readlines()

# TODO: use jinja or something
setup_template = open('../setup_template.xml').read()
# TODO: create condor template
condor_template= open('../condor_template.condor').read()

# create setup XML files and condor files
for simulation_number in range(len(lines)-1):
    for new_infra_investment in args.new_infra_investment:
        for maintenance in args.maintenance:
            with open('setup_nii%s_mii%s_%s_%s.xml' % (new_infra_investment,
                                                       maintenance,
                                                       args.landscape,
                                                       simulation_number), 'w') as setupfile, \
                open('submit_nii%s_mii%s_%s_%s.condor' % (new_infra_investment,
                                                          maintenance,
                                                          args.landscape,
                                                          simulation_number), 'w') as condorfile:
                setupfile.write(setup_template.format(simulation_number=simulation_number,
                                                      new_infra_investment=new_infra_investment,
                                                      maintenance=maintenance,
                                                      landscape=args.landscape))
                condorfile.write(condor_template.format(simulation_number=simulation_number,
                                                        new_infra_investment=new_infra_investment,
                                                        maintenance=maintenance,
                                                        landscape=args.landscape))
