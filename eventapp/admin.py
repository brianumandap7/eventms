from django.contrib import admin
from .models import events_details
from import_export.admin import ImportExportModelAdmin, ExportActionMixin

class exportSurvey(ExportActionMixin, admin.ModelAdmin):
	pass
# Register your models here.

admin.site.register(events_details, exportSurvey)


