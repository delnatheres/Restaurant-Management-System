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
    path('add_employee/', views.add_employee, name='add_employee'),
    path('employee_success/', views.employee_success, name='employee_success'),
    path('customer_dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('order/<int:item_id>/', views.place_order, name='place_order'),
    path('reservation/', views.make_reservation, name='make_reservation'),
    path('feedback/', views.submit_feedback, name='submit_feedback'),
    path('add_menu_item/', views.add_menu_item, name='add_menu_item'),
    path('orders/', views.customer_orders, name='customer_orders'),
    path('view_menu/', views.view_menu, name='view_menu'),
    path('menu_items/', views.menu_item_list, name='menu_item_list'),
    path('edit_menu_item/<int:id>/', views.edit_menu_item, name='edit_menu_item'),  # Correct this line
    path('add_menu_item/', views.add_menu_item, name='add_menu_item'),
    path('delete_menu_item/<int:id>/', views.delete_menu_item, name='delete_menu_item'), 
    path('categories/', views.view_category, name='view_category'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:cid>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:cid>/', views.delete_category, name='delete_category'),
    path('subcategories/', views.view_subcategory, name='view_subcategory'),
    path('subcategories/add/', views.add_subcategory, name='add_subcategory'),
    path('subcategories/edit/<int:subcategory_id>/', views.edit_subcategory, name='edit_subcategory'),
    path('subcategories/delete/<int:subcategory_id>/', views.delete_subcategory, name='delete_subcategory'),
    path('deactivate_user/<int:id>/', views.deactivate_user, name='deactivate_user'),
    path('activate_user/<int:id>/', views.activate_user, name='activate_user'),
    path('view_employees/', views.view_employees, name='view_employees'),  # New URL pattern
    path('employee-success/', views.employee_success, name='employee_success'),
    path('edit_employee/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    path('delete_employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),







     
    path('menu_items/', views.menu_item_list, name='menu_item_list'),
    path('edit_menu_item/<int:id>/', views.edit_menu_item, name='edit_menu_item'),  # Ensure this line is correct
    path('delete_menu_item/<int:id>/', views.delete_menu_item, name='delete_menu_item'),

   ]


