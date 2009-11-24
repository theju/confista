from django.db import models
from tagging.fields import TagField
from django.contrib.auth.models import User

class Topic(models.Model):
    name = models.CharField(max_length = 150)

    def __unicode__(self):
        return self.name

class Level(models.Model):
    name = models.CharField(max_length = 150)

    def __unicode__(self):
        return self.name

class Talk(models.Model):
    title       = models.CharField(max_length = 150)
    speakers    = models.ManyToManyField(User, 
                                         related_name="speakers",
                                         blank = True, null = True)
    abstract    = models.TextField()
    topic       = models.ForeignKey(Topic)
    tags        = TagField(max_length = 255)
    level       = models.ForeignKey(Level)
    accepted    = models.BooleanField(default = False)
    scheduled   = models.BooleanField(default = False)

    def __unicode__(self):
        return "%s : %s" %(self.topic, self.title)
