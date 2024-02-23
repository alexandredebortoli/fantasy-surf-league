from django.contrib import admin

from fantasy.models import League, Prediction, User, Event, Surfer

admin.site.register(User)
admin.site.register(League)
admin.site.register(Prediction)
admin.site.register(Event)
admin.site.register(Surfer)
