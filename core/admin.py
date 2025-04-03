from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Event, Testimonial, EventFeature, EventMedia, Itinerary, EventRegistration, Payment
from decouple import config
import resend

resend.api_key = config('RESEND_API')
admin.site.unregister(Group)


@admin.action(description="Confirm Full Payment")
def confirm_full_payment(modeladmin, request, queryset):
    for registration in queryset:
        registration.payment_status = 'completed'
        registration.confirmed_full_payment = True
        registration.save()


@admin.action(description="Confirm Part Payment")
def confirm_part_payment(modeladmin, request, queryset):
    for registration in queryset:
        registration.payment_status = 'part'
        registration.confirmed_part_payment = True
        registration.save()
        # Send email with remaining amount
        send_confirmation_email(registration, full_payment=False)


def send_confirmation_email(registration, full_payment=True):
    event = registration.event
    if full_payment:
        subject = f"Payment Confirmed for {event.title}"
        message = f"Dear {registration.first_name},\n\nYour full payment has been confirmed for {event.title}. Thank you!"
    else:
        remaining_amount = float(event.price) - float(event.pay_in_part)
        subject = f"Part Payment Confirmed for {event.title}"
        message = (
            f"Dear {registration.first_name},<br>"
            f"Your part payment has been confirmed for {event.title}.<br> "
            f"The remaining amount to be paid is ${remaining_amount:.2f}. "
            f"Please complete your payment by {event.complete_payment_before}."
            f"<h5>Payment link: {event.complete_payment_before}.</h5>"
        )
    try:
        resend.Emails.send({
            "from": "Your Event Payment <no-reply@iatwexperience.com>",  # Replace with your verified domain email
            "to": [registration.email],
            "subject": subject,
            "html": message,
        })
        print(f"Email sent to {registration.email}")
    except Exception as e:
        print(f"Failed to send email to {registration.email}: {e}")       


class EventMediaInline(admin.TabularInline):
    model = EventMedia
    extra = 1

class EventFeatureInline(admin.TabularInline):
    model = EventFeature
    extra = 1

class EventMediaAdmin(admin.ModelAdmin):
    list_display = ('event', 'media_type')
    list_filter = ('event', 'media_type')
    search_fields = ('event__title', 'title')
    list_per_page = 10  

class ItineraryInline(admin.TabularInline):
    model = Itinerary
    extra = 1  # Number of empty forms to display

class EventAdmin(admin.ModelAdmin):
    inlines = [EventMediaInline, EventFeatureInline, ItineraryInline]
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


class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone_number', 'event','payment_status', 'created_at')
    list_filter = ('event', 'created_at')
    search_fields = ('first_name', 'email')
    list_per_page = 10
    actions = [confirm_full_payment, confirm_part_payment]


admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(EventFeature, EventFeatureAdmin)
admin.site.register(EventMedia, EventMediaAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventRegistration, EventRegistrationAdmin)
