from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # URL pattern for the Django admin site
    path('', include('myapp.urls')),  # Include URLs from the app named 'myapp'
    
]
