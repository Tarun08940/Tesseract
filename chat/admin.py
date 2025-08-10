

# Register your models here.
from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content', 'timestamp')  # Columns in admin list view
    list_filter = ('user', 'timestamp')  # Sidebar filters
    search_fields = ('content', 'user__username')  # Search box
    ordering = ('-timestamp',)  # Newest messages first
