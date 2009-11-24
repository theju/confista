from talk.models import Topic, Level, Talk
from django.contrib import admin

class TopicAdmin(admin.ModelAdmin):
    pass

class LevelAdmin(admin.ModelAdmin):
    pass

class TalkAdmin(admin.ModelAdmin):
    pass

admin.site.register(Topic, TopicAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Talk,  TalkAdmin)
