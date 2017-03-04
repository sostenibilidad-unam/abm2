


python sim_setup.py --db_url postgresql+psycopg2://fidel@localhost/netlogo --sacmex_matrix ../data/DF101215_GOV_AP\ modificado\ PNAS.limit.csv --xochimilco_matrix ../data/X062916_OTR_a.limit.csv --iztapalapa_matrix ../data/I080316_OTR.limit.csv --contreras_matrix ../data/MC080416_OTR_a.limit.csv




## a sample session

First go into ipython thusly:

    $ ipython -i try.py

Then you might instance an aheb and a sacmex

	a=session.query(model.AGEB).get(5158)
	s=model.SACMEX()
	s.update_criteria_max()
	a.update_d_reparation(criteria_max=s.criteria_max)
