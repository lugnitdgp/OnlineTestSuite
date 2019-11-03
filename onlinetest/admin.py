from django.contrib import admin
from django.contrib.auth.models import User
from onlinetest.models import Question, Answer, Profile, Config

class ProfileAdmin(admin.ModelAdmin):
    change_form_template = "admin/custom_change_form.html"

    list_display = ['full_name','user','time_left']
    search_fields = ['full_name']
    actions = ['increase_time_by_10']

    def increase_time_by_10(self, req, queryset):
        for profile in queryset:
            profile.time_left += 600
            profile.save()
    
    increase_time_by_10.short_description = "Increase time by 10 min"

    def get_dynamic_info(self, object_id):
        questions = Question.objects.all()
        p = Profile.objects.get(id=object_id)
        answers = Answer.objects.filter(user=p.user)
    
        already_submitted = []
        for q in questions:
            ans = answers.filter(question=q).first()
            if ans:
                already_submitted.append(ans.text)
            else:
                already_submitted.append("N/A")

        respon = []
        for i in range(max(len(questions), len(already_submitted))):
            respon.append([questions[i], already_submitted[i]])

        return respon

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['responses'] = self.get_dynamic_info(object_id=object_id)
        return super(ProfileAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)


admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Config)