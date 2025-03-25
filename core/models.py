from django.db import models
from django.utils import timezone
from datetime import date
from django.utils.text import slugify
from django.urls import reverse
import cloudinary
from cloudinary.models import CloudinaryField
          
cloudinary.config( 
  cloud_name = "dl7u4nm7l",
  api_key = "883756833185195", 
  api_secret = "9dd_1LrMmKMq4yQG7zWwVAk87n0"
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
    file = models.FileField(upload_to='event_media/')
    thumbnail = models.ImageField(upload_to='event_thumbnails/', blank=True, null=True)
    title = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Event media'

    def __str__(self):
        return f"{self.event.title} - {self.get_media_type_display()}"

    def save(self, *args, **kwargs):
        # Ensure only one featured media per event
        if self.is_featured:
            EventMedia.objects.filter(event=self.event, is_featured=True).exclude(id=self.id).update(is_featured=False)
        super().save(*args, **kwargs)

class Event(models.Model):
    EVENT_STATUS = (
        ('upcoming', 'Upcoming'),
        ('past', 'Past'),
    )

    title = models.CharField(max_length=200)
    slug = models.UUIDField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    image = CloudinaryField(folder="event-images")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    event_date = models.DateField()
    group_size = models.IntegerField(default=10)
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