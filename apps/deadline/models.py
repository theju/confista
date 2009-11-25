from django.db import models
from django.conf import settings
if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

class Deadline(models.Model):
    code_name = models.CharField(max_length = 255, unique = True)
    descr     = models.CharField(max_length = 255)
    expiry    = models.DateTimeField()

    def __unicode__(self):
        return "%s expires on %s" %(self.descr, self.expiry)

def deadline_added(sender, instance, **kwargs):
    if notification:
        users = [ii.user for ii in notification.NoticeSetting.objects.filter(notice_type__label="deadlines_notification")]
        notification.send(users, "deadlines_notification",{"descr": instance})
models.signals.post_save.connect(deadline_added, sender=Deadline)
