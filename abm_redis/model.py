import redis
from astra import models

db = redis.StrictRedis(host='katsina2', decode_responses=True)


class AGEB(models.Model):

    database = db
    
    cvegeo = models.CharField()
    pobtot = models.IntegerField()
    vph_aguadv = models.CharField()
    vph_aguafv = models.CharField()
    vph_drenaj = models.CharField()
    vph_nodren = models.CharField()
    total_ench = models.CharField()
    mean_encha = models.CharField()
    kmeans5 = models.IntegerField()
    precip = models.IntegerField()
    hund = models.CharField()
    edad_infra = models.CharField()
    zonas = models.CharField()
    i05_ingres = models.CharField()
    ageb_id = models.CharField()
    fallain = models.CharField()
    presmed = models.CharField()
    faltain = models.CharField()
    petdels = models.CharField()
    escasez = models.CharField()
    subside = models.CharField()
    disease_bu = models.CharField()

    protestant = models.BooleanField()
    
    d_infra = models.CharField()
    
    t = models.IntegerField()

    def update_protesta(self):
        if random.random() < self.d_infra:
            self.protestant = True
        else:
            self.protestant = False

    def deteriora(self):
        if self.d_infra < 1.0:
            self.d_infra = random.uniform(1.01, 1.1) * self.d_infra

    def accion_colectiva(self):
        if self.deteriora_infra > 0:
            self.d_infra = random.uniform(0.9, 1) * self.d_infra

    def repara_infra(self, cuanto):
        self.d_infra -= cuanto


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

    # def repara_infras(self):
    #     for a in session.query(AGEB).filter(AGEB.protestant==True).order_by(AGEB.d_infra.asc()).all():
    #         self.repara_infra(a)

    # def repara_infra(self, ageb):
    #     cuanto = random.uniform(0.7, 0.8) * ageb.d_infra
    #     ageb.repara_infra(cuanto)
    #     session.commit()

    def __repr__(self):
        return "<SACMEX%s>" % self.id
    
