from django.contrib import admin

from fantasy.models import League, Prediction, User

admin.site.register(User)
admin.site.register(League)
admin.site.register(Prediction)
