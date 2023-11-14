from django.contrib import admin
from .models import events_details, UserProfile, AttendanceMonitoring, UserLogs, HistoricalUserLogs, HistoricalEventLogs, EventLogs, EventParticipants, Historicalevents_details, ecert, ipsurl, qform
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

admin.site.register(EventParticipants, exportSurvey)

admin.site.register(Historicalevents_details, exportSurvey)

admin.site.register(ecert, exportSurvey)

admin.site.register(ipsurl, exportSurvey)

admin.site.register(qform, exportSurvey)