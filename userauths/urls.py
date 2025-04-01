from django.urls import path
from . import views

app_name = 'userauths'

urlpatterns = [
    path('sign-up/', views.sign_up, name='register'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
]