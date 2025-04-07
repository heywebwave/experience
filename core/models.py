from django.db import models
from django.utils import timezone
from datetime import date
from django.utils.text import slugify
from django.urls import reverse
import cloudinary
from cloudinary.models import CloudinaryField
from userauths.models import CustomUser  
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField 
          
cloudinary.config( 
  cloud_name = "dl7u4nm7l",
  api_key = "883756833185195", 
  api_secret = "9dd_1LrMmKMq4yQG7zWwVAk87n0",
  secure=True  # This ensures all URLs are generated with HTTPS
)
# Create your models here.
class EventFeature(models.Model):
    name = models.CharField(max_length=100)
    is_included = models.BooleanField(default=True)
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='features')

    def __str__(self):
        return f"{self.name} ({'Included' if self.is_included else 'Not Included'})"

    def not_included(self):
        return not self.is_included

class EventMedia(models.Model):
    MEDIA_TYPES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )

    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='media')
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPES)
    # For images: use Cloudinary
    image = CloudinaryField(folder="event-images", null=True, blank=True)
    # For videos: store Vimeo URL
    video_url = models.URLField(max_length=255, null=True, blank=True, 
                              help_text="Enter Vimeo video URL (e.g., https://vimeo.com/123456789)")
    title = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Event media'

    def __str__(self):
        return f"{self.event.title} - {self.get_media_type_display()}"

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

    @property
    def vimeo_embed_url(self):
        """Convert Vimeo URL to embed URL"""
        if self.video_url and 'vimeo.com' in self.video_url:
            video_id = self.video_url.split('/')[-1]
            return f"https://player.vimeo.com/video/{video_id}"
        return None

class Event(models.Model):
    EVENT_STATUS = (
        ('upcoming', 'Upcoming'),
        ('past', 'Past'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    image = CloudinaryField(folder="event-images", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    event_date = models.DateField()
    group_size = models.IntegerField(default=10)
    pay_in_part = models.DecimalField(max_digits=10, decimal_places=2)
    complete_payment_before = models.DateField()
    full_payment_link = models.URLField(max_length=500, blank=True)
    part_payment_link = models.URLField(max_length=500, blank=True)
    complete_part_payment_link = models.URLField(max_length=500, blank=True)
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=EVENT_STATUS, default='upcoming')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-event_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Event.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        
        if self.event_date < date.today():
            self.status = 'past'
        else:
            self.status = 'upcoming'
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete the image from Cloudinary before deleting the Blog object
        if self.image:
            # Get the public ID of the image from Cloudinary
            public_id = self.image.public_id
            # Delete the image from Cloudinary
            cloudinary.uploader.destroy(public_id)
        # Call the parent class delete method to delete the Blog object
        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'slug': self.slug})

    @property
    def is_past(self):
        return self.event_date < date.today()
    
    @classmethod
    def update_all_event_status(cls):
        today = date.today()
        # Update past events
        cls.objects.filter(event_date__lt=today, status='upcoming').update(status='past')
        # Update upcoming events (in case any were manually set to past)
        cls.objects.filter(event_date__gte=today, status='past').update(status='upcoming')

    @property
    def featured_media(self):
        """Returns the featured media or the first media item"""
        featured = self.media.filter(is_featured=True).first()
        if not featured:
            featured = self.media.first()
        return featured

    @property
    def video(self):
        """Returns the first video"""
        return self.media.filter(media_type='video').first()

    @property
    def images(self):
        """Returns all images"""
        return self.media.filter(media_type='image')

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    image = CloudinaryField(folder="testimonials")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='testimonials')
    testimonial_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def delete(self, *args, **kwargs):
        # Delete the image from Cloudinary before deleting the Testimonial object
        if self.image:
            # Get the public ID of the image from Cloudinary
            public_id = self.image.public_id
            # Delete the image from Cloudinary  
            cloudinary.uploader.destroy(public_id)
        # Call the parent class delete method to delete the Testimonial object
        super().delete(*args, **kwargs)


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Testimonial by {self.name} for {self.event.title}"

class Itinerary(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='itineraries')
    day = models.PositiveIntegerField()  # Day number (e.g., 1, 2, 3, etc.)
    description = models.TextField()  # Description of the day's itinerary
    image = CloudinaryField(folder="itineraries")  # Image for the itinerary

    class Meta:
        ordering = ['day']  # Order by day number
        unique_together = ('event', 'day')  # Ensure no duplicate days for the same event

    def __str__(self):
        return f"Itinerary for {self.event.title} - Day {self.day}"
    

class EventRegistration(models.Model):

    PAYMENT_STATUS_CHOICES = (
        ('part', 'Part Payment'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    # Personal Information
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='registrations')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    organization = models.CharField(max_length=200, blank=True)
    job_title = models.CharField(max_length=200, blank=True)
    country = CountryField()
    phone_number = models.CharField(max_length=20, blank=True)

    # Conference Preferences
    sessions = models.JSONField(default=list)  # Store selected sessions
    attend_all_days = models.BooleanField()
    goals_expectations = models.TextField(blank=True)

    # Accommodation & Travel
    need_accommodation = models.BooleanField()
    need_transportation = models.BooleanField()
    roommate_preference = models.CharField(max_length=200, blank=True)
    arrival_date = models.DateField()
    departure_date = models.DateField()

    # Dietary and Medical Information
    dietary_restrictions = models.JSONField(default=list, blank=True)  # Vegetarian, Vegan, Gluten-Free, etc.
    medical_conditions = models.TextField(blank=True)  # Medical conditions or mobility needs

    # Emergency Contact Information
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_relationship = models.CharField(max_length=100, blank=True)
    emergency_contact_phone =  models.CharField(max_length=20, blank=True)


    # Additional Information
    how_heard_about_event = models.JSONField(default=list, blank=True)  # Website, Social Media, Referral, Others
    interested_in_volunteering = models.BooleanField(null=True, blank=True)  # Yes/No for volunteering

    # Event Reference
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    confirmed_part_payment = models.BooleanField(default=False)
    confirmed_full_payment = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.event.title}"


class Payment(models.Model):
    PAYMENT_TYPE_CHOICES = (
        ('full', 'Full Payment'),
        ('part', 'Part Payment'),
    )
    
    PAYMENT_STATUS_CHOICES = (
        ('part', 'Part Payment'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPE_CHOICES)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    stripe_payment_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.title} - {self.payment_type}"