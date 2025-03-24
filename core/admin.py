from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Event
from .models import Testimonial

admin.site.unregister(Group)

class EventAdmin(admin.ModelAdmin): 
    list_display = ('title', 'event_date', 'status')
    list_filter = ('status',)
    search_fields = ('title', 'description')
    list_per_page = 10

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'testimonial_text', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'testimonial_text')
    list_per_page = 10

admin.site.register(Event, EventAdmin)
admin.site.register(Testimonial, TestimonialAdmin)





