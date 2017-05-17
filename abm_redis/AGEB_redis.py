import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)

class AGEB_redis:

	deterioro = 0
	protestando = False

	def __init__(self, pk=None):
		if pk:
			self.pk = pk
			self.getAGEB()
		else:
			self.pk = self.createNewId()

	def createNewId(self):
		r.incr('ageb_ids')
		return r.get('ageb_ids')

	def getAGEB(self):
		existing = r.hgetall('ageb:'+str(self.pk))
		if 'deterioro' in existing:
			self.deterioro = existing['deterioro']
		else:
			self.deterioro = 0
		if 'protestando' in existing:
			self.protestando = existing['protestando']
		else:
			self.protestando = False

	def save(self):
		r.hmset('ageb:'+str(self.pk), {'deterioro': self.deterioro, 'protestando': self.protestando})
