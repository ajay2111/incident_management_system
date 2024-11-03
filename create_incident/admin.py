from django.contrib import admin
from .models import User, Incident

# Register your models here.

admin.site.register(User)
admin.site.register(Incident)

