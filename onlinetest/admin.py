from django.contrib import admin
from onlinetest.models import Question, Answer, Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name','user','time_left']
    actions = ['increase_time_by_10']

    def increase_time_by_10(self, req, queryset):
        for profile in queryset:
            profile.time_left += 600
            profile.save()
    
    increase_time_by_10.short_description = "Increase time by 10 min"

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Profile, ProfileAdmin)
