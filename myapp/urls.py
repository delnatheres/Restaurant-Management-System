from django.urls import path
from .views import *
urlpatterns = [
    path('', index_view, name='index'),  # Root URL for index
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),
    path('menu/', menu_view, name='menu'),
    path('sign_in/', sign_in_view, name='sign_in'),
    path('login/', login_view, name='login'),
    path('admin_dashboard/', admin_dashboard_view, name='admin_dashboard'),
    path('forgot_password/', forgot_password, name= 'forgot_password'),
    path('reset-password/<str:token>/', reset_password, name='reset_password'), 
 
        # Other URLs...
]
