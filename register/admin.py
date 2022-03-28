from django.contrib import admin

from .models import RegisterCode


@admin.register(RegisterCode)
class RegisterCodeAdmin(admin.ModelAdmin):
    model = RegisterCode
    list_display = ('__str__', 'used')
    list_filter = ('used',)
