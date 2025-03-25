from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Event, Testimonial, EventFeature, EventMedia

admin.site.unregister(Group)

class EventMediaInline(admin.TabularInline):
    model = EventMedia
    extra = 1
    fields = ('media_type', 'file', 'thumbnail', 'title', 'order', 'is_featured')

class EventFeatureInline(admin.TabularInline):
    model = EventFeature
    extra = 1

class EventMediaAdmin(admin.ModelAdmin):
    list_display = ('event', 'media_type', 'is_featured')
    list_filter = ('event', 'media_type')
    search_fields = ('event__title', 'title')
    list_per_page = 10  

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [EventMediaInline, EventFeatureInline]
    list_display = ('title', 'event_date', 'status', 'location')
    list_filter = ('status', 'event_date')
    search_fields = ('title', 'description', 'location')
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 10

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'testimonial_text', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'testimonial_text')
    list_per_page = 10

class EventFeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_included', 'event')
    list_filter = ('event',)
    search_fields = ('name',)
    list_per_page = 10

admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(EventFeature, EventFeatureAdmin)
admin.site.register(EventMedia, EventMediaAdmin)




