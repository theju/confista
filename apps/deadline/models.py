from django.db import models

class Deadline(models.Model):
    code_name = models.CharField(max_length = 255, unique = True)
    descr     = models.CharField(max_length = 255)
    expiry    = models.DateTimeField()

    def __unicode__(self):
        return "%s expires on %s" %(self.descr, self.expiry)
