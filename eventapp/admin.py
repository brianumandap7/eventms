from django.contrib import admin
from .models import events_details, UserProfile
from import_export.admin import ImportExportModelAdmin, ExportActionMixin #package

class exportSurvey(ExportActionMixin, admin.ModelAdmin): #class or function
	pass
# Register your models here.

admin.site.register(events_details, exportSurvey)

admin.site.register(UserProfile, exportSurvey)


