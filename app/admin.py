from django.contrib import admin
from .models import Rating, Comic

admin.site.register([Rating, Comic])