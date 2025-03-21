from django.shortcuts import render

app_name = 'core'
# Create your views here.
def index(request):
    return render(request, 'core/index.html')

