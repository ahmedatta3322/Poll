from django.contrib import admin
from .models import Poll, Choice

# Register your models here.


class PollAdmin(admin.ModelAdmin):
    pass


class ChoiceAdmin(admin.ModelAdmin):
    pass


admin.site.register(Poll, PollAdmin)
admin.site.register(Choice, ChoiceAdmin)
