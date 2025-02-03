from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Login, User,SignIn
from .forms import PasswordResetRequestForm  # Import both forms
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from .forms import EmployeeForm
from .models import Employee, Login
from django.contrib.auth.decorators import login_required
from .models import MenuItem, Order
from .models import Category
from .models import Category, SubCategory
from .models import Order
from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Login
from .models import MenuItem
import re


from .models import Customer, Order


from .models import Login, User, SignIn


from .models import Employee, EmployeeDashboard
from .models import EmployeeDashboard, Employee, LeaveRequest, Order,Cart,Feedback






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

def terms_and_conditions(request):
    return render(request, 'terms_and_conditions.html')


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
        # Retrieve customer name from the form input
        customer_name = request.POST.get('customer_name')  # Ensure the input name is correct in the form
        feedback_data = request.POST.get('comments')  # Retrieve comments
        ratings = request.POST.get('rating')  # Retrieve ratings

        # Save feedback to the database with customer name
        feedback = Feedback(
            customer_name=customer_name,  # Save customer name
            comments=feedback_data,       # Save comments
            rating=ratings                # Save rating
        )
        feedback.save()  # Save the feedback instance

        if feedback:
            # Add a success message after feedback is submitted
            messages.success(request, 'Feedback submitted successfully!')
            return redirect('feedback_success')  # Redirect after successful submission

    # Render the feedback form for GET requests
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

        # Validate that the category name only contains letters and spaces
        if cname:
            if re.match("^[A-Za-z\s]+$", cname):  # Allows letters and spaces
                Category.objects.create(cname=cname, status=status)
                messages.success(request, 'Category added successfully!')
                return redirect('view_category')
            else:
                messages.error(request, 'Category name should only contain letters and spaces.')
        else:
            messages.error(request, 'Category name is required.')

    return render(request, 'admin/add_category.html')


def edit_category(request, cid):
    category = get_object_or_404(Category, cid=cid)
    
    if request.method == 'POST':
        # Get the new values from the form
        cname = request.POST.get('cname')
        status = request.POST.get('status') == 'on'

        # Validate that the category name only contains letters and spaces
        if cname:
            if re.match("^[A-Za-z\s]+$", cname):  # Allows letters and spaces
                category.cname = cname
                category.status = status
                category.save()
                messages.success(request, 'Category updated successfully!')
                return redirect('view_category')
            else:
                messages.error(request, 'Category name should only contain letters and spaces.')
        else:
            messages.error(request, 'Category name is required.')

    # Render the form with the current category data
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

        # Validate that the subcategory name only contains letters and spaces
        if scname:
            if re.match("^[A-Za-z\s]+$", scname):  # Allows letters and spaces
                SubCategory.objects.create(scname=scname, cid_id=cid, status=status)
                messages.success(request, 'Subcategory added successfully.')
                return redirect('view_subcategory')
            else:
                messages.error(request, 'Subcategory name should only contain letters and spaces.')
        else:
            messages.error(request, 'Subcategory name is required.')

    # Fetch categories for the dropdown
    categories = Category.objects.all()
    return render(request, 'admin/add_subcategory.html', {'categories': categories})



def edit_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)

    if request.method == 'POST':
        scname = request.POST.get('scname')
        cid = request.POST.get('cid')
        status = request.POST.get('status') == 'on'

        # Validate that the subcategory name only contains letters and spaces and has a maximum length of 16
        if scname:
            if len(scname) <= 16:  # Check for maximum length of 16
                if re.match("^[A-Za-z\s]+$", scname):  # Allows letters and spaces
                    subcategory.scname = scname
                    subcategory.cid_id = cid
                    subcategory.status = status
                    subcategory.save()
                    messages.success(request, 'Subcategory updated successfully.')
                    return redirect('view_subcategory')
                else:
                    messages.error(request, 'Subcategory name should only contain letters and spaces.')
            else:
                messages.error(request, 'Subcategory name should not exceed 16 characters.')
        else:
            messages.error(request, 'Subcategory name is required.')

    # Fetch categories for the dropdown
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
    # Check if an ID for a specific menu item is provided
    if menu_item_id:
        menu_item_instance = get_object_or_404(MenuItem, id=menu_item_id)
        menu_items = None  # Since we're fetching a specific item, no list is needed
    else:
        # If no specific ID is provided, handle search and listing of menu items
        query = request.GET.get('search', '')
        menu_items = MenuItem.objects.all()

        # Apply search filter if a query is present
        if query:
            menu_items = menu_items.filter(name__icontains=query)

        menu_item_instance = None  # No single menu item fetched when listing

    context = {
        'menu_item_instance': menu_item_instance,
        'menu_items': menu_items,
        'query': query,
    }

    return render(request, 'customer/menu_item.html', context)




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
        rating = request.POST.get('rating')  # Assuming the rating is passed from the form
        feedback = Feedback(customer_name=request.user.username, comments=feedback_text, rating=rating)
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
    
    
    

    
# Add a menu item to the cart
def add_to_cart(request, menu_item_id):
    # Get the customer from the session
    customer_id = request.session.get('customer_id')
    
    if customer_id is None:
        messages.error(request, 'You must be logged in to add items to the cart.')
        return redirect('login')  # Redirect to login if no customer is logged in

    # Fetch the customer using the customer_id from the session
    customer = get_object_or_404(SignIn, pk=customer_id)

    # Fetch the menu item to be added to the cart
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)

    # Get the quantity from the POST data (default to 1 if no quantity is provided)
    quantity = int(request.POST.get('quantity', 1))

    # Check if the menu item is already in the customer's cart
    cart_item, created = Cart.objects.get_or_create(
        customer=customer,  # The logged-in customer
        menu_item=menu_item,  # The menu item to be added
        defaults={'quantity': quantity}  # Set default quantity if it's a new entry
    )

    if not created:
        # If the menu item already exists in the cart, update the quantity
        cart_item.quantity += quantity  # Increment the quantity
        cart_item.save()

    # Redirect to the cart view with a success message
    messages.success(request, 'Menu item added to cart successfully.')
    return redirect('view_cart')  # Redirect to the cart page




# View the cart
def viewcart(request):
    # Get the customer ID from the session
    customer_id = request.session.get('customer_id')
    
    if customer_id is None:
        # If the customer is not logged in, redirect to the login page
        messages.error(request, 'You must be logged in to view the cart.')
        return redirect('login')

    # Fetch the customer using the customer ID from the session
    customer = get_object_or_404(SignIn, pk=customer_id)

    # Fetch the cart items for the customer
    cart_items = Cart.objects.filter(customer=customer)

    # Calculate the total price of the cart items (assuming Cart model has a price or related field)
    total_price = sum([item.menu_item.price * item.quantity for item in cart_items])
    request.session['totalprice'] = float(total_price)
    # Context to pass to the template
    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    
    # Render the cart view with the context
    return render(request, 'customer/view_cart.html', context)




# Update the quantity of a menu item in the cart
def update_cart(request, cart_id):
    if request.method == 'POST':
        # Get the customer ID from the session
        customer_id = request.session.get('customer_id')

        if customer_id is None:
            messages.error(request, 'You must be logged in to update your cart.')
            return redirect('login')  # Redirect to login if not logged in

        # Fetch the cart item by its ID and make sure it belongs to the logged-in customer
        cart_item = get_object_or_404(Cart, pk=cart_id, customer_id=customer_id)

        # Get the new quantity from POST data, default to 1 if not provided
        quantity = int(request.POST.get('quantity', 1))

        if quantity > 0:
            # Update the cart item quantity if valid
            cart_item.quantity = quantity
            cart_item.save()  # Save the changes
            messages.success(request, 'Cart updated successfully.')
        else:
            # If quantity is zero or negative, optionally remove the item
            cart_item.delete()
            messages.success(request, f"{cart_item.menu_item.name} removed from cart due to invalid quantity.")

        return redirect('view_cart')  # Redirect to the cart view



# Remove a menu item from the cart
def delete_from_cart(request, cart_id):
    # Get the customer ID from the session
    customer_id = request.session.get('customer_id')
    
    if customer_id is None:
        messages.error(request, 'You must be logged in to modify your cart.')
        return redirect('login')  # Redirect to login if the customer is not logged in

    # Fetch the cart item by its ID and make sure it belongs to the logged-in customer
    cart_item = get_object_or_404(Cart, pk=cart_id, customer_id=customer_id)
    
    # Store the name of the menu item for the success message
    item_name = cart_item.menu_item.name
    
    # Delete the cart item
    cart_item.delete()
    
    # Success message
    messages.success(request, f"{item_name} removed from cart.")
    
    # Redirect to the cart view
    return redirect('view_cart')





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






from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, Order, OrderItem, SignIn  # Adjust import based on your actual models
from django.core.mail import send_mail
from django.conf import settings

def check_out(request):
    user = None
    try:
        # Fetch user based on session ID (convert to int if needed)
        user_id = int(request.session.get('user_id'))
        print("user",user_id)  
        user = SignIn.objects.get(id=user_id)
        print(user)
    except (ValueError, SignIn.DoesNotExist):
        user = None  # Set user to None if an error occurs

    # Fetch cart items for the logged-in user
    cart_items = Cart.objects.filter(customer=user) if user else []
    
    # Calculate the total price of the items in the cart
    total_price = sum(item.get_total_price() for item in cart_items)

    if request.method == 'POST':
        # Get contact and payment method from the form data
        contact = request.POST.get('contact', '')
        print(contact)
        payment_method = request.POST.get('payment_method', '')

        # Create the order if the user is logged in
        if user:
            # Create a new Order object
            order = Order.objects.create(
                customer=user,  # Assuming customer is ForeignKey to SignIn
                name=user.name if hasattr(user, 'name') else 'Guest',  # Ensure 'name' field exists
                contact=contact,
                email=user.email if hasattr(user, 'email') else '',  # Ensure 'email' field exists
                place=user.place if hasattr(user, 'place') else '',  # Ensure 'place' field exists
                total_price=total_price,
                payment_method=payment_method,
                status='pending'  # Assuming 'status' field exists in Order
            )

            # Create OrderItem instances for each cart item
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    menu_item=item.menu_item,  # Assuming 'menu_item' is ForeignKey in Cart
                    quantity=item.quantity,
                    price=item.menu_item.price  # Store the price at the time of order
                )


                

            # Clear the cart after placing the order
            cart_items.delete()

            # Redirect to order summary after placing the order
            messages.success(request, 'Order placed successfully!')
            return redirect('order_summary', order_id=order.id)
        else:
            # Show error message if user is not logged in
            error_message = "Please log in to place your order."
            return render(request, 'customer/check_out.html', {
                'error_message': error_message,
                'cart_items': cart_items,
                'total_price': total_price
            })
    user_id = int(request.session.get('customer_id'))
    print("user",user_id)  
    user = SignIn.objects.get(id=user_id)
    print(user)
# Render the checkout page with user and cart details
    return render(request, 'customer/check_out.html', {
        'user': user,
        'cart_items': cart_items,
        'total_price': total_price
    })
    
    
    
def place_order(request):
    if request.method == 'POST':
        # Fetch payment details and contact information from the POST request
        payment_method = request.POST.get('payment_method', 'N/A')
        contact = request.POST.get('contact', 'N/A')
        name = request.POST.get('customer_name', 'Guest')  # Use 'Guest' if name is not provided
        email = request.POST.get('email', None)
        place = request.POST.get('place', None)

        # Fetch the user's cart items
        cart_items = Cart.objects.all()  # Adjust this line according to how you identify carts

        # Check if there are items in the cart
        if not cart_items.exists():
            # If no items in the cart, redirect to the checkout page
            return redirect('check_out')

        # Calculate the total price
        total_price = sum(item.get_total_price() for item in cart_items)

        # Try to fetch or create the customer
        try:
            if email:  # If an email is provided
                customer, created = SignIn.objects.get_or_create(
                    email=email,
                    defaults={'name': name}  # If a new customer is created, set the name
                )
            else:  # If no email is provided, use a placeholder email
                customer, created = SignIn.objects.get_or_create(
                    email='guest@example.com',
                    defaults={'name': name}  # If a new customer is created, set the name
                )

        except IntegrityError:
            # Handle error if any issue occurs while creating/fetching the customer
            return redirect('check_out')

        # Create a new order
        order = Order.objects.create(
            customer=customer,  # Use the created or existing customer
            contact=contact,
            email=customer.email,  # Use the email from the customer object
            name=customer.name,  # Use the name from the customer object
            total_price=total_price,
            payment_method=payment_method,
            place=place,
            status='pending'  # Set initial status
        )

        # Add cart items to the order
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                menu_item=item.menu_item,
                quantity=item.quantity,
                price=item.menu_item.price
            )

        # Clear the user's cart after the order is placed
        cart_items.delete()

        # Prepare order details for the email
        order_details = (
            f"Order ID: {order.id}\n"
            f"Total Price: Rs. {total_price}\n"
            f"Payment Method: {payment_method}\n"
        )

        # Send the order confirmation email
        send_order_confirmation_email(user_email=customer.email, order=order)

        # Redirect to the order summary page with the order ID
        return redirect('order_summary', order_id=order.id)

    # If not a POST request, redirect to the checkout page
    return redirect('check_out')



from django.core.mail import send_mail
from django.conf import settings

def send_order_confirmation_email(user_email, order):
    subject = 'Order Confirmation'
    message = (
        f'Your order has been placed successfully!\n\n'
        f'Order ID: {order.id}\n'
        f'Total Price: Rs. {order.total_price}\n'
        f'Payment Method: {order.payment_method}'
    )
    from_email = settings.EMAIL_HOST_USER

    send_mail(
        subject,
        message,
        from_email,
        [user_email],
        fail_silently=False,
    )



import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import razorpay

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@csrf_exempt
def create_order(request):
    if request.method == "POST":
        # Example of fetching cart items, adjust according to your implementation
        cart_items = request.session.get('cart', [])  # Assuming 'cart' holds your items
        total_amount = 0

        for item in cart_items:
            # Assuming item contains 'price' and 'quantity'
            total_amount += item['price'] * item['quantity']  # Calculate total amount

        total_amount_in_paise = total_amount  # Convert to paise
        razorpay_order = razorpay_client.order.create({
            "amount": total_amount, 
            "currency": "INR", 
            "payment_capture": "1"
        })

        return JsonResponse({
            "order_id": razorpay_order['id'],
            "amount": total_amount_in_paise  # Return amount for use in the payment page
        })


@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            razorpay_client.utility.verify_payment_signature({
                'razorpay_order_id': data['order_id'],
                'razorpay_payment_id': data['payment_id'],
                'razorpay_signature': data['signature']
            })
            # Payment is successful
            return JsonResponse({"status": "success"})
        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({"status": "failure"})


from django.shortcuts import render

def payment_view(request):
    # Handle the payment logic here
    totalprice = request.session.get('totalprice', 0) 
    amount_in_paise = totalprice * 100
    
    return render(request, 'customer/payment.html',{'amount': amount_in_paise,})  # Adjust the template name as necessary





def order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.order_items.all()

    total_price = sum(item.price * item.quantity for item in order_items)
    formatted_total_price = f"{total_price:.2f}"

    context = {
        'order': order,
        'order_items': order_items,
        'total_price': formatted_total_price,
        'payment_method': order.payment_method,
    }

    return render(request, 'customer/order_summary.html', context)



def order_history(request):
    # Check if the user is logged in
    if request.user.is_authenticated:
        # Use email from the authenticated user
        email = request.user.email
        # Retrieve all orders associated with the logged-in user
        orders = Order.objects.filter(customer__email=email).prefetch_related('order_items__menu_item')
    else:
        # Use session or other method to track guest orders if applicable
        # For example, assuming a session-based customer ID is being used for guests:
        customer_id = request.session.get('customer_id')
        if customer_id:
            orders = Order.objects.filter(customer__id=customer_id).prefetch_related('order_items__menu_item')
            email = "Guest"
        else:
            orders = []
            email = "Guest"

    # Prepare context based on whether orders exist
    if orders:
        context = {
            'orders': orders,
            'email': email
        }
    else:
        context = {
            'message': 'No orders found for your account.' if request.user.is_authenticated or customer_id else 'Please log in or place an order.',
            'email': email
        }

    return render(request, 'customer/order_history.html', context)




def view_order(request):
    # Fetch all orders ordered by date
    orders = Order.objects.all().order_by('-ordered_at')  
    return render(request, 'admin/view_order.html', {'orders': orders})

def view_order(request):
    # Fetch all orders ordered by date
    orders = Order.objects.all().order_by('-ordered_at')  
    return render(request, 'employee/view_order.html', {'orders': orders})







from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TableReservation
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime, date
from .models import TableReservation

def reserve_table(request):
    if request.method == 'POST':
        # Retrieve data from the form
        customer_name = request.POST.get('customer_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        reservation_date = request.POST.get('reservation_date')
        reservation_time = request.POST.get('reservation_time')  # Now in AM/PM format
        number_of_guests = request.POST.get('number_of_guests')
        special_requests = request.POST.get('special_requests', '')

        # Validate phone number
        if not phone.isdigit() or len(phone) > 10:
            messages.error(request, "Invalid phone number. Please enter up to 10 digits only.")
            return redirect('reserve_table')

        # Validate number of guests
        try:
            number_of_guests = int(number_of_guests)
            if number_of_guests < 1 or number_of_guests > 10:
                messages.error(request, "Number of guests must be between 1 and 10.")
                return redirect('reserve_table')
        except ValueError:
            messages.error(request, "Invalid number of guests.")
            return redirect('reserve_table')

        # Validate and parse date
        try:
            reservation_date = datetime.strptime(reservation_date, "%Y-%m-%d").date()
            if reservation_date < date.today():
                messages.error(request, "You can only reserve a table for today or future dates.")
                return redirect('reserve_table')
        except ValueError:
            messages.error(request, "Invalid date format. Please try again.")
            return redirect('reserve_table')

        # Convert 12-hour AM/PM time format to 24-hour format
        try:
            reservation_time = datetime.strptime(reservation_time, "%I:%M %p").time()
        except ValueError:
            messages.error(request, "Invalid time format. Please select a valid time slot.")
            return redirect('reserve_table')

        # Create reservation and save to the database
        reservation = TableReservation.objects.create(
            customer_name=customer_name,
            email=email,
            phone=phone,
            reservation_date=reservation_date,
            reservation_time=reservation_time,
            number_of_guests=number_of_guests,
            special_requests=special_requests
        )

        # Convert date and time objects to strings
        reservation_date_str = reservation_date.strftime("%Y-%m-%d")
        reservation_time_str = reservation_time.strftime("%I:%M %p")  # Store in 12-hour format for session

        # Save the reservation to the session
        reservations = request.session.get('reservations', [])
        reservations.append({
            'customer_name': customer_name,
            'email': email,
            'phone': phone,
            'reservation_date': reservation_date_str,
            'reservation_time': reservation_time_str,
            'number_of_guests': number_of_guests,
            'special_requests': special_requests,
        })
        request.session['reservations'] = reservations

        # Show success message
        messages.success(request, "Your reservation has been successfully added!")
        return redirect('reservation_history')

    return render(request, 'customer/reserve_table.html')







from django.shortcuts import render, redirect
from django.contrib import messages

def view_reservation(request):
    # Get the latest reservation from the session
    reservations = request.session.get('reservations', [])
    if not reservations:
        messages.error(request, "No reservation found.")
        return redirect('reserve_table')

    # Fetch the most recent reservation
    latest_reservation = reservations[-1]

    return render(request, 'customer/view_reservation.html', {'reservation': latest_reservation})




from django.shortcuts import render

def reservation_history(request):
    # Fetch reservations from session
    reservations = request.session.get('reservations', [])
    return render(request, 'customer/reservation_history.html', {
        'reservations': reservations,
    })



def table_reservation(request):
    # Fetch reservations from session
    reservations = request.session.get('reservations', [])
    return render(request, 'admin/table_reservation.html', {
        'reservations': reservations,
    })

def table_reservation_history(request):
    # Fetch reservations from session
    reservations = request.session.get('reservations', [])
    return render(request, 'employee/table_reservation_history.html', {
        'reservations': reservations,
    })





from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages

def table_reservation(request):
    # Mock data for reservations if session data doesn't exist
    if 'reservations' not in request.session:
        request.session['reservations'] = [
            {
                'id': 1,
                'customer_name': 'John Doe',
                'email': 'john@example.com',
                'phone': '1234567890',
                'reservation_date': '2025-01-30',
                'reservation_time': '19:00',
                'number_of_guests': 4,
                'special_requests': 'Window seat',
                'status': 'Pending',
            },
            {
                'id': 2,
                'customer_name': 'Jane Smith',
                'email': 'jane@example.com',
                'phone': '9876543210',
                'reservation_date': '2025-01-31',
                'reservation_time': '20:00',
                'number_of_guests': 2,
                'special_requests': 'Vegan menu',
                'status': 'Pending',
            }
        ]

    reservations = request.session['reservations']
    return render(request, 'admin/table_reservation.html', {
        'reservations': reservations,
    })


def update_reservation_status(request):
    if request.method == 'POST':
        reservation_id = request.POST.get('reservation_id')
        action = request.POST.get('action')

        if not reservation_id or not action:
            messages.error(request, "Invalid request data.")
            return redirect('table_reservation')

        try:
            # Fetch reservations from the session (or database if using one)
            reservations = request.session.get('reservations', [])
            for reservation in reservations:
                if str(reservation['id']) == str(reservation_id):
                    if action == 'approve':
                        reservation['status'] = 'Approved'
                        messages.success(request, f"Reservation {reservation_id} has been approved.")
                    elif action == 'reject':
                        reservation['status'] = 'Rejected'
                        messages.error(request, f"Reservation {reservation_id} has been rejected.")
                    break
            else:
                messages.error(request, "Reservation not found.")

            # Save updated reservations back to the session
            request.session['reservations'] = reservations

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return redirect('table_reservation')














from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
import google.generativeai as genai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure the Generative AI client
API_KEY = "AIzaSyBnNAb8qvTChM3TVTPKqIYEug3SlSzSO3Q"
genai.configure(api_key=API_KEY)

# Update the system prompt to specify Indian Rupees
SYSTEM_PROMPT = """You are a helpful Restaurant Assistant for our restaurant management system. 
Your role is to assist customers with:

1. Menu Information:
   - Dish recommendations with prices in Indian Rupees (₹)
   - Price ranges (e.g., ₹200-₹500 for main courses)
   - Special dietary options (vegetarian, vegan, gluten-free)
   - Daily specials and their prices

2. Reservation Help:
   - Table booking process
   - Minimum booking amounts if applicable
   - Cancellation policies
   - Special event booking rates

3. General Information:
   - Restaurant hours
   - Location and directions
   - Payment methods (UPI, cards, cash)
   - Minimum order values
   - Delivery charges if applicable

4. Special Services:
   - Catering packages with pricing
   - Private dining costs
   - Group booking rates
   - Special occasion celebration packages

Please format responses in a clear, structured way using:
- Show all prices in Indian Rupees with the ₹ symbol
- Use bullet points for lists
- *text* for emphasis
- Clear sections with line breaks
- Professional and friendly tone"""

@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')

        if not user_message:
            return JsonResponse({'error': 'No message provided'}, status=400)

        try:
            # Create the model
            model = genai.GenerativeModel("gemini-pro")

            # Add restaurant-specific context with Indian pricing
            restaurant_context = """
            Our restaurant offers:
            
            Menu Price Ranges:
            - Starters: ₹150 - ₹300
            - Main Course: ₹250 - ₹500
            - Desserts: ₹100 - ₹200
            - Beverages: ₹80 - ₹150
            
            Special Offers:
            - Lunch Buffet: ₹499 per person
            - Weekend Brunch: ₹699 per person
            - Happy Hours (4-6 PM): 20% off on beverages
            - Group Discount: 10% off for groups of 8 or more
            
            Minimum Orders:
            - Dine-in: No minimum order
            - Delivery: Minimum ₹300
            - Private Events: Starting from ₹15,000
            
            Payment Options:
            - All major credit/debit cards
            - UPI payments (PhonePe, Google Pay, Paytm)
            - Cash payments
            
            Opening Hours:
            - Monday to Friday: 11:00 AM - 10:00 PM
            - Saturday and Sunday: 10:00 AM - 11:00 PM
            
            Location: [Your Restaurant Address]
            Contact: [Your Restaurant Phone]
            """

            # Combine prompts and generate response
            formatted_prompt = f"{SYSTEM_PROMPT}\n\nRestaurant Context: {restaurant_context}\n\nCustomer Query: {user_message}"
            response = model.generate_content(formatted_prompt)

            # Format the response
            ai_message = response.text.replace('•', '&bull;')
            
            # Ensure ₹ symbol is displayed correctly
            ai_message = ai_message.replace('Rs.', '₹').replace('INR', '₹')
            
            logger.info(f"Generated response for: {user_message}")
            return JsonResponse({'response': ai_message})

        except Exception as e:
            logger.error(f"Error in restaurant chatbot: {str(e)}")
            return JsonResponse({
                'response': "I apologize, but I'm having trouble assisting you at the moment. Please try again or speak with our staff for immediate assistance."
            }, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=400)