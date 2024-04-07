from django.contrib import admin
from .models import ConvertConfig, Grade
# Register your models here.


class GradeInline(admin.TabularInline):
    model = Grade
    extra = 3


class ConfigAdmin(admin.ModelAdmin):
    fields = ["author", "config_name"]
    inlines = [GradeInline]


admin.site.register(ConvertConfig, ConfigAdmin)
