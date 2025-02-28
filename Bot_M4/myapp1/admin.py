from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('tel_id', 'name', 'email', 'phone')
    readonly_fields = ('tel_id', )
    list_filter = ['is_admin', 'is_blocked']
    search_fields = ['phone', 'name', 'email',]


@admin.register(Archive)
class UserAdmin(admin.ModelAdmin):
    list_display = ('tel_id', 'name', 'email')
    readonly_fields = ('tel_id', )
    list_filter = ['is_admin', 'is_blocked']
    search_fields = ['name', 'email']


@admin.register(Deleted)
class UserAdmin(admin.ModelAdmin):
    list_display = ('tel_id', 'name', 'email')
    readonly_fields = ('tel_id',)
    list_filter = ['is_admin', 'is_blocked']
    search_fields = ['name', 'email']


@admin.register(UserProgress)
class UserAdmin(admin.ModelAdmin):
    list_display = ('tel_id', 'name', 'email')
    readonly_fields = ('tel_id', 'progress')
    search_fields = ['name', 'email']


@admin.register(Payment)
class UserAdmin(admin.ModelAdmin):
    list_display = ('order_reference', 'email', 'transaction_status')
    search_fields = ['phone', 'email']
