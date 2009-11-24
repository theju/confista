from django.db import models

# TODO: Breaks DRY but can't think of
# anything for dynamicness.
class Menu_Item(models.Model):
    name = models.CharField(max_length = 50)
    link = models.CharField(max_length = 2048)
    login_to_view = models.BooleanField(default=False)
    open_in_new_window = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s : %s" %(self.name, 
                           self.link)
