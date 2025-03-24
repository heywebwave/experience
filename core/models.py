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