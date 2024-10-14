from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Login, User,SignIn
from .forms import PasswordResetRequestForm  # Import both forms
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from .forms import EmployeeForm
from .models import Employee, Login
from django.contrib.auth.decorators import login_required
from .models import MenuItem, Order,Feedback
from .models import Category
from .models import Category, SubCategory
from .models import Order
from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Login
from .models import MenuItem,Wishlist
import re

from .models import Feedback
from .models import Customer, Order


from .models import Login, User, SignIn


from .models import Employee, EmployeeDashboard
from .models import EmployeeDashboard, Employee, LeaveRequest, Order






def index_view(request):
    return render(request, 'index.html')

def sign_in_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        place = request.POST.get('place')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(f"Form Data: Name={name}, Place={place}, Email={email}, Password={password}")

        user=SignIn(name=name,email=email,password=password,place=place)
        user.save()
        if(user):
            messages.success(request, 'User created successfully')
            return redirect('login')
        else:
            messages.error(request, 'Failed to create user')
            return render(request, 'sign_in.html')
    return render(request, 'sign_in.html')


from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Login  # Make sure to import your Login model

from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Login  # Make sure to import your Login model


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check for admin credentials
        if email == 'admin@gmail.com' and password == 'admin123':
            messages.success(request, 'Welcome Admin!')
            request.session['user_id'] = 'admin' 
            return redirect('admin_dashboard')  # Redirect to admin dashboard
        
        # Attempt to retrieve the user by email and password
        try:
            login_obj = SignIn.objects.get(email=email, password=password)
            if login_obj.role == 'Employee':
                    # Fetch the employee data if the user is an employee
                    employee = Employee.objects.get(email=email)
                    request.session['employee_id'] = employee.employee_id
                    messages.success(request, 'Welcome Employee!')
                    return render(request, 'employee/employee_dashboard.html', {'employee': employee})
        
            else:
                # If the user is not an employee, they are treated as a customer
                messages.success(request, f'Welcome, {login_obj.name}!')
                request.session['customer_id'] = login_obj.id 
                return render(request, 'customer/customer_dashboard.html')  # Redirect to customer dashboard
            
        except SignIn.DoesNotExist:
            # If SignIn record does not exist
            messages.error(request, 'Invalid email or password.')
            return redirect('login')
    
    # If request method is not POST, simply return the login page
    return render(request, 'login.html')






def about_view(request):
    return render(request, 'about.html')

def contact_view(request):
    return render(request, 'contact.html')

def menu_view(request):
    return render(request, 'menu.html')



def forgot_password(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = Login.objects.get(email=email)
                # Generate a random token (you can customize this)
                reset_token = get_random_string(30)
                user.reset_token = reset_token
                user.save()
                
                # Send reset email (for now, let's print the link)
                reset_link = f"http://localhost:8000/reset-password/{reset_token}/"
                # Send the email
                subject = "Password Reset Request"
                message = f"Hi, please click the link below to reset your password:\n\n{reset_link}\n\nIf you did not request this, please ignore this email."
                from_email = 'delnatheres2025@mca.ajce.in'
                recipient_list = [email]
                
                send_mail(subject, message, from_email, recipient_list)
                
                messages.success(request, 'A password reset link has been sent to your email.')
                return redirect('/login/')
            except Login.DoesNotExist:
                messages.error(request, 'Email address not found')
    else:
        form = PasswordResetRequestForm()

    return render(request, 'password_reset_request.html', {'form': form})

def reset_password(request, token):
    try:
        user = Login.objects.get(reset_token=token)
    except Login.DoesNotExist:
        messages.error(request, 'Invalid or expired reset token')
        return redirect('/login/')
    
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password == confirm_password and len(password) >= 8:
            user.password = password  # Hash the password in a real-world scenario
            user.reset_token = ''  # Clear the reset token
            user.save()
            messages.success(request, 'Your password has been reset successfully')
            return redirect('/login/')
        else:
            messages.error(request, 'Passwords do not match or are not long enough')
    
    return render(request, 'password_reset.html')



def admin_dashboard_view(request):
    return render(request, 'admin/admin_dashboard.html')

def viewuser(request):
    person=SignIn.objects.all()
    return render(request,'admin/view_user.html',{"person":person})


import re
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Employee, SignIn  # Ensure you import necessary models

def add_employee(request):
    if request.method == "POST":
        name = request.POST.get('name')
        place = request.POST.get('place')
        phone = request.POST.get('phone')
        salary = request.POST.get('salary')
        status = request.POST.get('status') == 'True'  # Convert to boolean
        email = request.POST.get('email')  # Get email from POST data
        password = request.POST.get('password')  # Get password from POST data
        
        # Validate required fields
        if not name or not phone or not salary or not place or not email or not password:
            messages.error(request, "All fields are required.")
            return render(request, 'admin/add_employee.html')
        
        # Validate name (only letters and spaces)
        if not re.match("^[A-Za-z ]+$", name):
            messages.error(request, "Name should contain only letters and spaces.")
            return render(request, 'admin/add_employee.html')

        # Validate place (only letters and spaces)
        if not re.match("^[A-Za-z ]+$", place):
            messages.error(request, "Place should contain only letters and spaces.")
            return render(request, 'admin/add_employee.html')

        # Validate password requirements
        if not re.match(r'^(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*]).{8,}$', password):
            messages.error(request, "Password must contain at least 1 uppercase letter, 1 special character, 1 digit, and be at least 8 characters long.")
            return render(request, 'admin/add_employee.html')

        # Validate phone (optional, if needed)
        # Example: only digits allowed, length between 10 and 15
        if not re.match(r'^\d{10,15}$', phone):
            messages.error(request, "Phone number must contain only digits and be between 10 and 15 characters long.")
            return render(request, 'admin/add_employee.html')

        # Create SignIn and Employee instances if all validations pass
        if email:  # Ensure email is not empty
            # Create and save the SignIn instance
            login = SignIn(email=email, password=password, role="Employee")
            login.save()

            # Create and save the Employee instance
            employee = Employee(
                name=name,
                place=place,  # Only pass 'place' once
                phone=phone,
                salary=salary,
                status=status,
                email=email
            )
            employee.save()

            return redirect('employee_success')  # Redirect after successful form submission
        else:
            messages.error(request, "Email is required.")
    
    return render(request, 'admin/add_employee.html')





def employee_success(request):
    return render(request, 'admin/employee_success.html', {'employee_added': True})  # Pass a variable to indicate success



def view_employees(request):
    # Get the search query from the GET request
    search_query = request.GET.get('name', '')
    
    # Filter employees based on the search query
    if search_query:
        employees = Employee.objects.filter(name__icontains=search_query)  # Search by name
    else:
        employees = Employee.objects.all()  # Retrieve all employees if no search query
    
    # Prepare the context for rendering the template
    context = {
        'employees': employees
    }
    
    return render(request, 'admin/view_employees.html', context)


def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, employee_id=employee_id)

    if request.method == 'POST':
        employee.first_name = request.POST.get('first_name')
        employee.last_name = request.POST.get('last_name')
        employee.phone = request.POST.get('phone')
        employee.salary = request.POST.get('salary')
        employee.status = request.POST.get('status') == 'True'
        employee.save()
        return redirect('view_employees')

    return render(request, 'admin/edit_employee.html', {'employee': employee})



def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, employee_id=employee_id)

    if request.method == 'POST':
        employee.delete()
        return redirect('view_employees')

    return render(request, 'admin/delete_employee.html', {'employee': employee})



# Customer Dashboard

def customer_dashboard(request):
    menu_items = MenuItem.objects.filter(available=True)  # Show only available items
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')  # Show user's orders
    
    return render(request, 'customer/customer_dashboard.html', {'menu_items': menu_items, 'orders': orders})







# Submit Feedback
def submit_feedback(request):
    if request.method == 'POST':
        # Here you would typically process the feedback data
        customer_id = request.session.get('customer_id')
        feedback_data = request.POST.get('comments')  # Example of getting feedback data
        ratings=request.POST.get('rating')
        print("Ratings : ",ratings)
        # You can save this data to your database or handle it as needed
        feedback= Feedback(customer=customer_id,comments=feedback_data,rating=ratings)
        # Optionally, add a success message (if you want to notify the user)
        feedback.save()
        if feedback:
            messages.success(request, 'Feedback submitted successfully!')
            return redirect('feedback_success')  # Use the name of your success URL pattern

    # Render the feedback submission form for GET requests
    return render(request, 'customer/submit_feedback.html')


from django.shortcuts import render, redirect
from .models import Customer  # Make sure to import your Customer model if needed

def customer_dashboard(request):
    customer_id = request.user.id  # This will give you the logged-in user's ID
    return render(request, 'customer/customer_dashboard.html')


def feedback_success(request):
    return render(request, 'customer/feedback_success.html')


from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from .models import MenuItem

# Define the MenuItemForm directly in views.py
class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
        labels = {
            'name': 'Menu Item Name',
            'description': 'Description',
            'price': 'Price',
            'available': 'Available?',
        }

from django.shortcuts import render, redirect
from django.contrib import messages
def add_menu_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        available = request.POST.get('available') == 'on'
        image = request.FILES.get('image')  # Get the uploaded image file

        # Validation: Check if name and description contain numbers
        if re.search(r'\d', name):
            messages.error(request, 'Name must not contain numbers.')
            return render(request, 'admin/add_menu_items.html')

        if re.search(r'\d', description):
            messages.error(request, 'Description must not contain numbers.')
            return render(request, 'admin/add_menu_items.html')

        # Validation: Check if price is a valid number and not negative
        try:
            price = float(price)  # Convert price to float
            if price < 0:  # Check for negative price
                messages.error(request, 'Price must not be a negative number.')
                return render(request, 'admin/add_menu_items.html')
        except ValueError:
            messages.error(request, 'Price must be a valid number.')
            return render(request, 'admin/add_menu_items.html')

        # Create MenuItem
        MenuItem.objects.create(
            name=name,
            description=description,
            price=price,
            available=available,
            image=image  # Save the image
        )

        messages.success(request, 'Menu item added successfully.')
        return redirect('add_menu_item_success')  # Redirect to the success page

    return render(request, 'admin/add_menu_items.html')






def add_menu_item_success(request):
    # Optional: You can add a message if needed
    messages.info(request, 'You have successfully added a menu item.')
    return render(request, 'admin/add_menu_item_success.html') 



def customer_orders(request):
    # Your logic to fetch and display orders
    return render(request, 'orders.html')



def view_menu(request):
    # Get the search query from the request
    query = request.GET.get('search', '')
    
    # Fetch all menu items from the database
    if query:
        menu_items = MenuItem.objects.filter(name__icontains=query)  # Filter by name (case-insensitive)
    else:
        menu_items = MenuItem.objects.all()  # Fetch all if no search query
    
    return render(request, 'admin/view_menu.html', {'menu_items': menu_items, 'query': query})


# myapp/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import MenuItem

def edit_menu_item(request, id):
    menu_item = get_object_or_404(MenuItem, id=id)

    if request.method == 'POST':
        # Assuming you have a form to update the item's name
        menu_item.name = request.POST.get('name')
        menu_item.save()
        return redirect('menu_item_list')  # Redirect after saving

    return render(request, 'admin/edit_menu_item.html', {'menu_item': menu_item})



def edit_menu_item(request, id):
    menu_item = get_object_or_404(MenuItem, id=id)

    if request.method == 'POST':
        # Retrieve data from the form
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        available = request.POST.get('available') == 'True'  # Convert to boolean
        image = request.FILES.get('image')  # Get the uploaded image file

        # Validation: Check if name and description contain numbers
        if re.search(r'\d', name):
            messages.error(request, 'Name must not contain numbers.')
            return render(request, 'admin/edit_menu_item.html', {'menu_item': menu_item})

        if re.search(r'\d', description):
            messages.error(request, 'Description must not contain numbers.')
            return render(request, 'admin/edit_menu_item.html', {'menu_item': menu_item})

        # Validation: Check if price is a valid number and not negative
        try:
            price = float(price)  # Convert price to float
            if price < 0:  # Check for negative price
                messages.error(request, 'Price must not be a negative number.')
                return render(request, 'admin/edit_menu_item.html', {'menu_item': menu_item})
        except ValueError:
            messages.error(request, 'Price must be a valid number.')
            return render(request, 'admin/edit_menu_item.html', {'menu_item': menu_item})

        # Update MenuItem fields
        menu_item.name = name
        menu_item.description = description
        menu_item.price = price
        menu_item.available = available
        
        if image:  # Update image only if a new one is provided
            menu_item.image = image

        menu_item.save()  # Save changes to the database
        messages.success(request, 'Menu item updated successfully.')
        return redirect('menu_item_list')  # Redirect after saving

    return render(request, 'admin/edit_menu_item.html', {'menu_item': menu_item}) 


def menu_item_list(request):
    menu_items = MenuItem.objects.all()  # Retrieve all menu items from the database
    return render(request, 'admin/menu_item_list.html', {'menu_items': menu_items})  # Render the menu items template


def delete_menu_item(request, id):
    menu_item = get_object_or_404(MenuItem, id=id)  # Retrieve the menu item by its ID
    menu_item.delete()  # Delete the menu item from the database
    return redirect('menu_item_list')  # Redirect to the menu item list view




from django.shortcuts import render, get_object_or_404, redirect

# View to display all categories
def view_category(request):
    categories = Category.objects.all()  # Fetch all categories
    return render(request, 'admin/view_category.html', {'categories': categories})

def add_category(request):
    if request.method == 'POST':
        cname = request.POST.get('cname')
        status = request.POST.get('status') == 'on'

        # Validate that the category name does not contain numbers
        if cname:
            if cname.isalpha():  # Ensure that the category name only contains alphabetic characters
                Category.objects.create(cname=cname, status=status)
                messages.success(request, 'Category added successfully!')
                return redirect('view_category')
            else:
                messages.error(request, 'Category name should only contain alphabetic characters.')
        else:
            messages.error(request, 'Category name is required.')

    return render(request, 'admin/add_category.html')


# View to edit an existing category
def edit_category(request, cid):
    category = get_object_or_404(Category, cid=cid)
    if request.method == 'POST':
        category.cname = request.POST.get('cname')
        category.status = request.POST.get('status') == 'on'

        # Validate that the category name does not contain numbers
        if category.cname:
            if category.cname.isalpha():  # Ensure that the category name only contains alphabetic characters
                category.save()
                messages.success(request, 'Category updated successfully!')
                return redirect('view_category')
            else:
                messages.error(request, 'Category name should only contain alphabetic characters.')
        else:
            messages.error(request, 'Category name is required.')

    return render(request, 'admin/edit_category.html', {'category': category})



# View to delete a category
def delete_category(request, cid):
    category = get_object_or_404(Category, cid=cid)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('view_category')
    return render(request, 'admin/delete_category.html', {'category': category})



# View for listing all subcategories
def view_subcategory(request):
    subcategories = SubCategory.objects.all()
    return render(request, 'admin/view_subcategory.html', {'subcategories': subcategories})


def add_subcategory(request):
    if request.method == 'POST':
        scname = request.POST.get('scname')
        cid = request.POST.get('cid')
        status = request.POST.get('status') == 'on'  # Checkbox value handling

        # Validate that the subcategory name does not contain numbers
        if scname:
            if scname.isalpha():  # Ensure that the subcategory name only contains alphabetic characters
                SubCategory.objects.create(scname=scname, cid_id=cid, status=status)
                messages.success(request, 'Subcategory added successfully.')
                return redirect('view_subcategory')
            else:
                messages.error(request, 'Subcategory name should only contain alphabetic characters.')
        else:
            messages.error(request, 'Subcategory name is required.')

    categories = Category.objects.all()
    return render(request, 'admin/add_subcategory.html', {'categories': categories})


# View for editing a subcategory
def edit_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)

    if request.method == 'POST':
        scname = request.POST.get('scname')
        cid = request.POST.get('cid')
        status = request.POST.get('status') == 'on'

        # Validate that the subcategory name does not contain numbers
        if scname and scname.isalpha():  # Ensure it only contains alphabetic characters
            subcategory.scname = scname
            subcategory.cid_id = cid
            subcategory.status = status
            subcategory.save()
            messages.success(request, 'Subcategory updated successfully.')
            return redirect('view_subcategory')
        else:
            messages.error(request, 'Subcategory name should only contain alphabetic characters and cannot be empty.')

    categories = Category.objects.all()
    return render(request, 'admin/edit_subcategory.html', {'subcategory': subcategory, 'categories': categories})




# View for deleting a subcategory
def delete_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)

    if request.method == 'POST':
        subcategory.delete()
        messages.success(request, 'Subcategory deleted successfully.')
        return redirect('view_subcategory')

    return render(request, 'admin/delete_subcategory.html', {'subcategory': subcategory})



def deactivate_user(request, id):
    user = get_object_or_404(SignIn, id=id)
    
    # Deactivate the user
    user.status = 0  # Set status to 0 (deactivated)
    user.save()

    # Send email notification
    send_mail(
        "Account Deactivation Notice",
        f"Hello {user.name}, your account has been deactivated. If you wish to reactivate it, please contact support.",
        'delnatheres2025@mca.ajce.in',  # Change this to your email
        [user.email],
        fail_silently=False,
    )

    return redirect('view_user')  # Redirect to the sign-in details page

def activate_user(request, id):
    user = get_object_or_404(SignIn, id=id)
    
    # Activate the user
    user.status = 1  # Set status to 1 (activated)
    user.save()

    # Send email notification
    send_mail(
        "Account Reactivation Notice",
        f"Hello {user.name}, your account has been reactivated. Welcome back!",
        'delnatheres2025@mca.ajce.in',  # Change this to your email
        [user.email],
        fail_silently=False,
    )

    return redirect('view_user')  # Redirect to the sign-in details page





def menu_item(request, menu_item_id=None):
    # Fetch a specific menu item if an ID is provided, otherwise list all or search
    if menu_item_id:
        menu_item_instance = get_object_or_404(MenuItem, id=menu_item_id)
    else:
        query = request.GET.get('search', '')
        if query:
            menu_items = MenuItem.objects.filter(name__icontains=query)
        else:
            menu_items = MenuItem.objects.all()

    # Handle wishlist logic in POST request
    if request.method == 'POST':
        if 'add_to_wishlist' in request.POST:
            user_id = request.session.get('user_id')  # Assuming session stores user ID
            if user_id:
                user = User.objects.get(id=user_id)
                menu_item_instance = get_object_or_404(MenuItem, id=menu_item_id)
                wishlist_item, created = Wishlist.objects.get_or_create(user=user, menu_item=menu_item_instance)

                if created:
                    messages.success(request, 'Menu item added to your wishlist!')
                else:
                    messages.info(request, 'Menu item is already in your wishlist.')
            else:
                messages.error(request, 'You need to log in to add items to your wishlist.')

    context = {
        'menu_item_instance': menu_item_instance if menu_item_id else None,
        'menu_items': menu_items if not menu_item_id else None,
        'query': query if not menu_item_id else '',
    }

    return render(request, 'customer/menu_item.html', context)







def add_to_wishlist(request, menu_item_id):
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)
    Wishlist.objects.create(user=request.user, menu_item=menu_item)
    return redirect('wishlist')  


def view_wishlist(request):
    # Get the user's ID or set to None if not authenticated
    user_id = request.user.id if request.user.is_authenticated else None

    if user_id:
        # Retrieve wishlist items for the authenticated user
        wishlist_items = Wishlist.objects.filter(user_id=user_id)
    else:
        # Set wishlist_items to an empty queryset if the user is not authenticated
        wishlist_items = Wishlist.objects.none()

    return render(request, 'customer/wishlist.html', {'wishlist_items': wishlist_items})


def remove_from_wishlist(request):
    if request.method == 'POST':
        remove_item_id = request.POST.get('remove_item_id')
        try:
            item = Wishlist.objects.get(id=remove_item_id, user=request.user)
            item.delete()
            messages.success(request, 'Item removed from wishlist!')
        except Wishlist.DoesNotExist:
            messages.error(request, 'Item not found in your wishlist.')
    return redirect('view_wishlist')  # Redirect back to wishlist







# Place an Order
@login_required
def place_order(request, item_id):
    item = MenuItem.objects.get(id=item_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        Order.objects.create(customer=request.user, menu_item=item, quantity=quantity)
        messages.success(request, 'Order placed successfully!')
        return redirect('customer_dashboard')
    return render(request, 'customer/menu_item.html', {'item': item})



def menu_item_new(request):
    query = request.GET.get('search', '')
    if query:
        menu_items = MenuItem.objects.filter(name__icontains=query)
    else:
        menu_items = MenuItem.objects.all()

    context = {
        'menu_items': menu_items,
        'query': query,
    }
    return render(request, 'employee/menu_item_new.html', context)






from django.shortcuts import render, get_object_or_404
from .models import Employee  # Ensure you import your models

def employee_dashboard(request, employee_id):
    employee = get_object_or_404(Employee, employee_id=employee_id)  # Fetch the employee instance

    return render(request, 'employee/employee_dashboard.html', {'employee': employee})





from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import LeaveRequest, Employee  # Ensure you import your models

def create_leave_request(request, employee_id):
    # Retrieve the employee or return a 404 error if not found
    employee = get_object_or_404(Employee, employee_id=employee_id)  # Use `employee_id` as the field name

    if request.method == 'POST':
        leave_type = request.POST.get('leave_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')

        # Create a new leave request instance
        leave_request = LeaveRequest(
            employee=employee,  # Assign the employee object
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            reason=reason
        )
        leave_request.save()  # Save the leave request to the database

        # Redirect to a success page or the employee dashboard
        return redirect('employee_dashboard', employee_id=employee_id)  # Adjust if necessary

    # Render the leave request form if GET request
    return render(request, 'employee/create_leave_request.html', {'employee': employee})





def feedback_view(request):
    if request.method == 'POST':
        feedback_text = request.POST.get('feedback')
        feedback = Feedback(customer=request.user, feedback_text=feedback_text)
        feedback.save()
        return redirect('feedback_thankyou')  # Redirect to a thank you page
    return render(request, 'admin/feedback.html')

def view_feedback(request):
    feedback_list = Feedback.objects.all().order_by('-created_at')
    return render(request, 'admin/view_feedback.html', {'feedback_list': feedback_list})

def feedback_thankyou(request):
    return render(request, 'admin/feedback_thankyou.html')





from django.shortcuts import render, get_object_or_404, redirect
from .models import LeaveRequest

# Admin view for listing all leave requests
def view_leave_requests(request):
    leave_requests = LeaveRequest.objects.all().order_by('-start_date')  # Display all leave requests
    return render(request, 'admin/view_leave_requests.html', {'leave_requests': leave_requests})


# Admin action to approve or reject leave requests
def approve_leave_request(request, leave_request_id, action):
    leave_request = get_object_or_404(LeaveRequest, id=leave_request_id)
    
    if action == 'approve':
        leave_request.status = 'Approved'
    elif action == 'reject':
        leave_request.status = 'Rejected'
    
    leave_request.save()
    return redirect('view_leave_requests') 



def view_leave_status(request):
    # Get the search query from GET parameters
    search_query = request.GET.get('search', '')

    if search_query:
        # Filter leave requests by employee name if search query is present
        leave_requests = LeaveRequest.objects.filter(employee__name__icontains=search_query)
    else:
        # Fetch all leave requests if no search query is provided
        leave_requests = LeaveRequest.objects.all()

    # Check if there are no leave requests and add a message
    if not leave_requests.exists():
        messages.info(request, "No leave requests found for the given search.")

    # Render the template with leave requests and messages
    return render(request, 'employee/view_leave_status.html', {
        'leave_requests': leave_requests,
        'messages': messages.get_messages(request)  # Pass messages to the template
    })
    
    
    
    
    
    
    