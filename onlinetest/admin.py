from django.contrib import admin
from django.contrib.auth.models import User
from onlinetest.models import Question, Answer, Profile, Config

class ProfileAdmin(admin.ModelAdmin):

    change_form_template = "admin/change_view.html"

    list_display = ['full_name','user','time_left']
    actions = ['increase_time_by_10']

    def increase_time_by_10(self, req, queryset):
        for profile in queryset:
            profile.time_left += 600
            profile.save()
    
    increase_time_by_10.short_description = "Increase time by 10 min"

    def get_dynamic_info(self, object_id):
        questions = Question.objects.all()
        # for q in questions:
        #     print(q)
        p = Profile.objects.get(id=object_id)
        u = User.objects.get(username=p.user.username)
        # print(u)
        already_submitted = []
        for q in questions:
            already_submitted.append(Answer.objects.filter(question=q, user=u).values('text'))

        # print(len(already_submitted))
        respon = []
        for i in range(max(len(questions), len(already_submitted))):
            respon.append([questions[i], already_submitted[i]])
        for r in respon:
            if(r[1]):
                for i in r[1]:
                    r[0] = r[0].title
                    r[1] = i['text']
                    # print("{} {}".format(r[0], i['text']))
            else:
                r[0] = r[0].title
                r[1] = "NA"
                # print("{} {}".format(r[0], "NA"))

        return respon

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['osm_data'] = self.get_dynamic_info(object_id=object_id)
        # print(extra_context)
        return super(ProfileAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)


admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Config)