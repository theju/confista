from django.db import models
from talk.models import Talk

class Day(models.Model):
    date       = models.DateField()
    start_time = models.TimeField()
    end_time   = models.TimeField()

    def __unicode__(self):
        return self.date.strftime("%d-%B-%Y") 

    class Meta:
       ordering = ["date",]

class Hall(models.Model):
    name     = models.CharField(max_length=100,unique=True)
    location = models.CharField(max_length=100,unique=True)
    capacity = models.PositiveIntegerField()

    def __unicode__(self):
        return "%s : %s" %(self.name,self.capacity)
    

class Slot(models.Model):
    day        = models.ForeignKey(Day, related_name="conf_day")
    start_time = models.TimeField()
    end_time   = models.TimeField()
    hall       = models.ForeignKey(Hall, related_name="hall")
    talk       = models.ForeignKey(Talk, related_name="talk", 
                                   limit_choices_to = {"accepted": True, "scheduled": False})

    def save(self, force_insert=False, force_update=False):
        self.talk.scheduled = True
        self.talk.save()
        super(Slot, self).save(force_insert, force_update)
    
    def __unicode__(self):
        return "%s on %s starting at %s at %s" %(self.talk.title,
                                                 self.day.date.strftime("%d %B,%Y"),
                                                 self.start_time.strftime("%H:%M %p"),
                                                 self.hall.name)
