from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.base import View
from .models import CustomUser
from .forms import SignUpForm, SignInForm
import os



def sign_up(request):
    if request.method == "POST" and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        # Initialize the form with POST data
        form = SignUpForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')

            # Check if a user with the provided email already exists
            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({
                    'success': False,
                    'errors': {'email': 'A user with this email already exists.'},
                }, status=400)

            try:
                # Save the user
                user = form.save(commit=False)
                user.set_password(form.cleaned_data["password"])  # Hash the password
                user.save()

                # Log in the user
                login(request, user)

                # Return success response
                return JsonResponse({
                    'success': True,
                    'message': f"Hey {user.first_name}, your account has been created successfully.",
                    'redirect_url': '/',  # Adjust the redirect URL as needed
                }, status=201)

            except Exception as e:
                # Handle unexpected errors
                return JsonResponse({
                    'success': False,
                    'errors': {'detail': str(e)},
                }, status=400)

        # If the form is invalid, return the errors
        return JsonResponse({
            'success': False,
            'errors': form.errors,
        }, status=400)

    # Render the registration page for non-AJAX GET requests
    return JsonResponse({
            'success': False,
            'errors': "Invalid request method. Please use POST.",
        }, status=400)

def sign_in(request):
    if request.method == "POST":
        form = SignInForm(request.POST)
        
        # Validate the form
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            # Authenticate user
            user = authenticate(request, email=email, password=password)
            
            if user is None:
                return JsonResponse(
                    {'success': False, 'message': 'Invalid credentials.'}, 
                    status=401
                )
            
            # Check if the account is active
            if not user.is_active:
                return JsonResponse(
                    {'success': False, 'message': 'Account is inactive. Please contact support.'}, 
                    status=401
                )
            
            # Log in the user
            login(request, user)
            fullname = f"{user.full_name}"
            
            # Successful login response
            return JsonResponse(
                {'success': True, 'message': f"Welcome back, {fullname}!",'redirect_url': "/dashboard/"},
                status=200
            )
        
        # Handle form errors
        return JsonResponse(
            {'success': False, 'errors': form.errors}, 
            status=400
        )
    
    # Render the sign-in page for GET requests
    form = SignInForm()
    return JsonResponse({
            'success': False,
            'errors': "Invalid request method. Please use POST.",
        }, status=400)


def logout_view(request):
    logout(request)
    return redirect("core:index")

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'userauths/dashboard.html'
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'user': {
                    'email': request.user.email,
                    'first_name': request.user.first_name,
                    'last_name': request.user.last_name,
                    'country': request.user.country.name,
                    'phone_number': str(request.user.phone_number) if request.user.phone_number else None
                }
            })
        return super().get(request, *args, **kwargs)

