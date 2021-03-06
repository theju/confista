from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

class Occupation(models.Model):
    name = models.CharField(max_length = 255)

    def __unicode__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length = 150)

    def __unicode__(self):
        return self.name

class Delegate_Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    location = models.ForeignKey(Location, related_name="location", null=True, blank=True)
    website = models.URLField(null=True, blank=True, verify_exists=False)

    organization = models.CharField(max_length = 200, null = True, blank = True)
    occupation   = models.ForeignKey(Occupation, related_name = "occupation", null=True, blank=True)
    
    def __unicode__(self):
        return self.user.username

    def get_absolute_url(self):
        return ('profile_detail', None, {'username': self.user.username})
    get_absolute_url = models.permalink(get_absolute_url)

    def __unicode__(self):
        return "%s of %s" %(self.name, self.organization)

def create_profile(sender, instance=None, **kwargs):
    if instance is None:
        return
    profile, created = Delegate_Profile.objects.get_or_create(user=instance)

def delegate_registered(sender, instance=None, **kwargs):
    if notification and kwargs['created']:
        users = [ii.user for ii in notification.NoticeSetting.objects.filter(notice_type__label="delegate_registered")]
        notification.send(users, "delegate_registered", {"descr": "%s registered." %instance.username})

post_save.connect(create_profile, sender=User)
post_save.connect(delegate_registered, sender=User)
