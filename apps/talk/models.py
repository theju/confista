from django.db import models
from django.conf import settings
from tagging.fields import TagField
from django.contrib.auth.models import User
if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

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

def talk_added(sender, instance=None, **kwargs):
    if notification and kwargs['created']:
        users = [ii.user for ii in notification.NoticeSetting.objects.filter(notice_type__lable='talk_added')]
        notification.send(users, "talk_added", {"descr": "Talk with title \"%s\" added" %instance.title})

def talk_accepted(sender, instance=None, **kwargs):
    if notification and not kwargs['created'] and instance.accepted:
        users = [ii.user for ii in notification.NoticeSetting.objects.filter(notice_type__lable='talk_accepted')]
        notification.send(users, "talk_accepted", {"descr": "Talk with title \"%s\" accepted" %instance.title)

def talk_scheduled(sender, instance=None, **kwargs):
    if notification and not kwargs['created'] and instance.scheduled:
        users = [ii.user for ii in notification.NoticeSetting.objects.filter(notice_type__lable='talk_scheduled')]
        notification.send(users, "talk_scheduled", {"descr": "Talk with title \"%s\" scheduled" %instance.title)

models.signals.post_save.connect(talk_added,     sender=Talk)
models.signals.post_save.connect(talk_accepted,  sender=Talk)
models.signals.post_save.connect(talk_scheduled, sender=Talk)
