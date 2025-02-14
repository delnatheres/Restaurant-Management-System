from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index_view, name='index'),  # Root URL for index
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('terms-and-conditions/', views.terms_and_conditions, name='terms_and_conditions'),
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
    path('menu_item/', views.menu_item, name='menu_item'),  # Add this
    path('menu_item/<int:menu_item_id>/', views.menu_item, name='menu_item_with_id'),
    path('menu_item_new/', views.menu_item_new, name='menu_item_new'),
    path('feedback/', views.submit_feedback, name='submit_feedback'),  # URL for submitting feedback
    path('feedback_success/', views.feedback_success, name='feedback_success'),  # URL for success page
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),  # URL for the customer dashboard
    path('feedback/', views.feedback_view, name='feedback'),
    path('view_feedback/', views.view_feedback, name='view_feedback'),
    path('feedback_thankyou/', views.feedback_thankyou, name='feedback_thankyou'),
    path('add_menu_item/', views.add_menu_item, name='add_menu_item'),
    path('add_menu_item_success/', views.add_menu_item_success, name='add_menu_item_success'),
    path('view_leave_requests/', views.view_leave_requests, name='view_leave_requests'),
    path('approve_leave_request/<int:leave_request_id>/<str:action>/', views.approve_leave_request, name='approve_leave_request'),
    path('leave_requests/', views.view_leave_requests, name='view_leave_requests'),
    path('leave_requests/<int:leave_request_id>/<str:action>/', views.approve_leave_request, name='approve_leave_request'),
    path('view_leave_status/', views.view_leave_status, name='view_leave_status'),
    path('view_cart/', views.viewcart, name='view_cart'),  # View cart
    path('cart/add/<int:menu_item_id>/', views.add_to_cart, name='add_to_cart'),  # Add item to cart
    path('cart/update/<int:cart_id>/', views.update_cart, name='update_cart'),
    path('cart/delete/<int:cart_id>/', views.delete_from_cart, name='delete_from_cart'),  # Delete item from cart
    path('checkout/', views.check_out, name='check_out'),  # Shortened for clarity
    path('place-order/', views.place_order, name='place_order'),
    path('order-summary/<int:order_id>/', views.order_summary, name='order_summary'),
    path('order/<int:item_id>/', views.place_order, name='place_order'),
    path('order-history/', views.order_history, name='order_history'),
    path('view-order/', views.view_order, name='view_order'),
    path('dashboard/<int:employee_id>/', views.employee_dashboard, name='employee_dashboard'),
    path('employee_dashboard/<int:employee_id>/', views.employee_dashboard, name='employee_dashboard'),
    path('create_leave_request/<int:employee_id>/', views.create_leave_request, name='create_leave_request'),
    path('create_order/', views.create_order, name='create_order'),
    path('verify_payment/', views.verify_payment, name='verify_payment'),
    path('payment/', views.payment_view, name='payment_view'),
    path('reserve_table/', views.reserve_table, name='reserve_table'),
    path('reserve/', views.reserve_table, name='reserve_table'),
    path('view-reservation/', views.view_reservation, name='view_reservation'),
    path('reserve-table/', views.reserve_table, name='reserve_table'),
    path('reservation-history/', views.reservation_history, name='reservation_history'),
    path('table_reservation/', views.table_reservation, name='table_reservation'),
    path('table_reservation_history/', views.table_reservation_history, name='table_reservation_history'),
    path('table_reservation/', views.table_reservation, name='table_reservation'),
    path('update-reservation-status/', views.update_reservation_status, name='update_reservation_status'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('edit_reservation/', views.edit_reservation, name='edit_reservation'),
    path('cancel_reservation/', views.cancel_reservation, name='cancel_reservation'),
    


    path('voice-assistant/', views.voice_assistant, name='voice_assistant'),
    

    
]
if settings.DEBUG:
  urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)