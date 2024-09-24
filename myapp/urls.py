from django.urls import path
from . import views
urlpatterns = [
    path('', views.index_view, name='index'),  # Root URL for index
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('menu/', views.menu_view, name='menu'),
    path('sign_in/', views.sign_in_view, name='sign_in'),
    path('login/', views.login_view, name='login'),
    path('admin_dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('forgot_password/', views.forgot_password, name= 'forgot_password'),
    path('reset-password/<str:token>/', views.reset_password, name='reset_password'), 
    path('viewuser/',views.viewuser,name='view_user'),
   ]
