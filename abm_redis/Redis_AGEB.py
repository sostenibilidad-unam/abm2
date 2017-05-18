import random
import redis
umbral = 1.0
r = redis.StrictRedis(host='localhost', port=6379, db=0)

class Redis_AGEB:

	deterioro = 0
	protestando = False

	def __init__(self, pk=None):
		if pk:
			self.pk = pk

	def createNew(self):
		self.pk = self.createNewId()
		self.save()

	def createNewId(self):
		r.incr('ageb_ids')
		return r.get('ageb_ids')

	def getAGEB(self, pk=None):
		if pk:
			self.pk = pk
		existing = r.hgetall('ageb:'+str(self.pk))
		if 'deterioro' in existing:
			self.deterioro = float(existing['deterioro'])
		else:
			self.deterioro = 0
		if 'protestando' in existing:
			self.protestando = existing['protestando']
		else:
			self.protestando = False

	def save(self):
		r.hmset('ageb:'+str(self.pk), {'deterioro': self.deterioro, 'protestando': self.protestando})

	def runWearAndTear(self):
		self.deterioro += random.random()
		if self.deterioro > umbral:
			self.protestando = True
			r.zadd('ageb_reparar', self.deterioro, str(self.pk))
		self.save()
