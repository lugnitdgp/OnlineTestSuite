from django.contrib import admin
from django.contrib.auth.models import User
from onlinetest.models import Question, Answer, Profile, Config
from django.contrib.admin.models import LogEntry, ADDITION, DELETION, CHANGE
from django.urls import reverse, NoReverseMatch, path
from django.utils.html import format_html, escape
from django.contrib.contenttypes.models import ContentType

class ProfileAdmin(admin.ModelAdmin):
    change_form_template = "admin/custom_change_form.html"

    fields = ['user', 'time_left', 'full_name',
              'phone', 'rollno', 'remarks', 'selected', 'selected_for_task_round', 'priority']
    list_display = ['full_name', 'user', 'time_left',
                    'selected', 'selected_for_task_round']
    search_fields = ['full_name']
    actions = ['increase_time_by_10', 'set_priority']

    def increase_time_by_10(self, req, queryset):
        for profile in queryset:
            profile.time_left += 600
            profile.save()
    
    increase_time_by_10.short_description = "Increase time by 10 min"

    def set_priority(self, req, queryset):
        for profile in queryset:
            profile.priority = 5
            profile.save()

    set_priority.short_description = "Set priority to 5"

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

    def get_readonly_fields(self, request, obj=None):
        if obj and (not request.user.is_superuser):
            return ['user','time_left','full_name','rollno','phone']
        else:
            return []

    def get_updaters(self, object_id):
        ul = LogEntry.objects.filter(object_id=object_id, action_flag=CHANGE).order_by('action_time')
        res = {}
        for log in ul:
            res.update({ log.user : log.action_time })
        return res
    
    def get_viewers(self, request, object_id):
        p = Profile.objects.get(pk=object_id)
        p.viewed_by.add(request.user)
        p.save()

        return p.viewed_by.values_list('username', flat=True)


    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['responses'] = self.get_dynamic_info(object_id=object_id)
        
        # show who modified the profile
        extra_context['ulogs'] = self.get_updaters(object_id)
       
       # page viewers
        v = self.get_viewers(request, object_id)
        extra_context['viewers'] = ", ".join(v)

        return super(ProfileAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)


## This Section Handels the Log Entry

action_names = {
    ADDITION: 'Addition',
    CHANGE:   'Change',
    DELETION: 'Deletion',
}


class FilterBase(admin.SimpleListFilter):
    def queryset(self, request, queryset):
        if self.value():
            dictionary = dict(((self.parameter_name, self.value()),))
            return queryset.filter(**dictionary)


class ActionFilter(FilterBase):
    title = 'action'
    parameter_name = 'action_flag'

    def lookups(self, request, model_admin):
        return action_names.items()


class UserFilter(FilterBase):
    """Use this filter to only show current users, who appear in the log."""
    title = 'user'
    parameter_name = 'user_id'

    def lookups(self, request, model_admin):
        return tuple((u.id, u.username)
                     for u in User.objects.filter(pk__in=LogEntry.objects.values_list('user_id').distinct())
                     )


class AdminFilter(UserFilter):
    """Use this filter to only show current Superusers."""
    title = 'admin'

    def lookups(self, request, model_admin):
        return tuple((u.id, u.username) for u in User.objects.filter(is_superuser=True))


class StaffFilter(UserFilter):
    """Use this filter to only show current Staff members."""
    title = 'staff'

    def lookups(self, request, model_admin):
        return tuple((u.id, u.username) for u in User.objects.filter(is_staff=True))


class LogEntryAdmin(admin.ModelAdmin):

    date_hierarchy = 'action_time'

    readonly_fields = [f.name for f in LogEntry._meta.get_fields()]

    list_filter = [
        UserFilter,
        ActionFilter,
        'content_type',
        # 'user',
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_description',
        'change_message',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != 'POST'

    def has_delete_permission(self, request, obj=None):
        return False

    def object_link(self, obj):
        ct = obj.content_type
        repr_ = escape(obj.object_repr)
        try:
            href = reverse('admin:%s_%s_change' %
                           (ct.app_label, ct.model), args=[obj.object_id])
            link = '<a href="%s">%s</a>' % (href, repr_)
        except NoReverseMatch:
            link = repr_
        return format_html(link) if obj.action_flag != DELETION else repr_
    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = 'object'

    def queryset(self, request):
        return super(LogEntryAdmin, self).queryset(request) \
            .prefetch_related('content_type')

    def action_description(self, obj):
        return action_names[obj.action_flag]
    action_description.short_description = 'Action'


admin.site.register(LogEntry, LogEntryAdmin)
# Logentry code Ends

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Config)
