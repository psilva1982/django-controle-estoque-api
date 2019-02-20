from django.contrib import admin

from estoque.models import Local
from estoque.models import Medida

# Register your models here.
admin.site.register(Local)
admin.site.register(Medida)