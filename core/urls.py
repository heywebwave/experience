from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.index, name='index'),
    path('in/', views.index1, name='index1'),
    path('about/', views.about, name='about'),
    path('cron/update-event-status/', views.update_event_status, name='update_event_status'),
    path('events/', views.event_list, name='event_list'),
    path('event/<slug:slug>/', views.event_detail, name='event_detail'),
    path('registration/', views.event_registration_view, name='registration'),
    path('event/<slug:slug>/media/', views.event_media, name='event_media'),
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
]
