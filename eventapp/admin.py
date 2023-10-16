from django.contrib import admin
from .models import events_details, UserProfile, AttendanceMonitoring, UserLogs, HistoricalUserLogs, HistoricalEventLogs, EventLogs
from import_export.admin import ImportExportModelAdmin, ExportActionMixin #package
from django.contrib.admin.models import LogEntry


class exportSurvey(ExportActionMixin, admin.ModelAdmin): #class or function
	pass
# Register your models here.

admin.site.register(events_details, exportSurvey)

admin.site.register(UserProfile, exportSurvey)

admin.site.register(AttendanceMonitoring, exportSurvey)

admin.site.register(UserLogs, exportSurvey)

admin.site.register(LogEntry, exportSurvey)

admin.site.register(HistoricalUserLogs, exportSurvey)

admin.site.register(HistoricalEventLogs, exportSurvey)

admin.site.register(EventLogs, exportSurvey)
