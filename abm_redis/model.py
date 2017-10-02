import redis
from astra import models
import random

db = redis.StrictRedis(host='katsina2', decode_responses=True)


class AGEB(models.Model):

    database = db

    protestant = models.BooleanField()
    
    d_infra = models.CharField()
    
    t = models.IntegerField()

    def update_protesta(self):
        if random.random() < float(self.d_infra):
            self.protestant = True
        else:
            self.protestant = False

    def deteriora(self):
        if float(self.d_infra) < 1.0:
            self.d_infra = random.uniform(1.01, 1.1) * float(self.d_infra)

    def repara_infra(self, cuanto):
        self.d_infra = float(self.d_infra) - cuanto


    def sync_run(self, t):
        self.deteriora()
        self.update_protesta()
        self.t = t

    def async_run(self):
        self.deteriora()
        self.update_protesta()

    def __repr__(self):
        if self.protestant:
            return "<A%s! %s t=%s>" % (self.pk, self.d_infra, self.t)
        else:
            return "<A%s  %s t=%s>" % (self.pk, self.d_infra, self.t)



class SACMEX(models.Model):

    database = db
    
    status = models.CharField() # play, pause, stop

    t = models.IntegerField()

    def get_protestantes(self):
        protestantes = []
        for k in range(1,len(db.keys("astra::ageb*protestant"))+1):
            a = AGEB(pk=k)
            if a.protestant:
                protestantes.append(k)
        return protestantes

    def count_outdated(self):
        outdated = []
        for k in range(1,len(db.keys("astra::ageb*protestant"))+1):
            a = AGEB(pk=k)
            if a.t != self.t:
                outdated.append(k)
        return len(outdated)

    
    def repara_infras(self):
        for k in self.get_protestantes():
            a = AGEB(pk=k)
            self.repara_ageb(a)     

    def repara_ageb(self, ageb):
        cuanto = random.uniform(0.7, 0.8) * float(ageb.d_infra)
        ageb.repara_infra(cuanto)


    def __repr__(self):
        return "<SACMEX%s>" % self.id
    
