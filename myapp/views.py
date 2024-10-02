from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Login, User,SignIn
from .forms import PasswordResetRequestForm  # Import both forms
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from .forms import EmployeeForm
from .models import Employee, Login
from django.contrib.auth.decorators import login_required
from .models import MenuItem, Order, Reservation, Feedback
from .models import Category
from .models import Category, SubCategory
from .models import Order
from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Login






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
            return redirect('admin_dashboard')  # Redirect to admin dashboard
        
        # Attempt to retrieve the user by email and password
        try:
            login_obj = SignIn.objects.get(email=email, password=password)
            if login_obj:
            # For regular users
                messages.success(request, f'Welcome, {login_obj.name}!')
                return render (request,'customer/customer_dashboard.html') # Redirect to user homepage

        except SignIn.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            return redirect('login')
    else:
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



def add_employee(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        salary = request.POST.get('salary')
        status = request.POST.get('status') == 'True'  # Convert to boolean
        email = request.POST.get('email')  # Get email from POST data
        password = request.POST.get('password')  # Get password from POST data

        # Validate required fields
        if not first_name or not last_name or not phone or not salary:
            messages.error(request, "All fields are required.")
            return render(request, 'admin/add_employee.html')

        if email and password:  # Ensure email and password are not empty
            # Create and save the Login instance
            login = Login.objects.create(email=email, password=password)

            # Create and save the Employee instance
            employee = Employee(
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                salary=salary,
                status=status,
                login=login  # Associate the login with the employee
            )
            employee.save()

            return redirect('employee_success')  # Redirect after successful form submission
        else:
            # Handle the case where email or password is missing
            messages.error(request, "Email and password are required.")
    
    return render(request, 'admin/add_employee.html')


def employee_success(request):
    return render(request, 'admin/employee_success.html', {'employee_added': True})  # Pass a variable to indicate success



def view_employees(request):
    employees = Employee.objects.all()  # Fetch all employees
    return render(request, 'admin/view_employees.html', {'employees': employees})




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
@login_required
def customer_dashboard(request):
    menu_items = MenuItem.objects.filter(available=True)  # Show only available items
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')  # Show user's orders
    
    return render(request, 'customer/customer_dashboard.html', {'menu_items': menu_items, 'orders': orders})

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


# Make a Reservation
@login_required
def make_reservation(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        guests = request.POST.get('guests')
        Reservation.objects.create(customer=request.user, date=date, time=time, guests=guests)
        return redirect('customer_dashboard')
    return render(request, 'customer/make_reservation.html')

# Submit Feedback
@login_required
def submit_feedback(request):
    if request.method == 'POST':
        comments = request.POST['comments']
        rating = request.POST['rating']
        Feedback.objects.create(customer=request.user, comments=comments, rating=rating)
        return redirect('customer_dashboard')
    return render(request, 'customer/submit_feedback.html')


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
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Menu item added successfully!')
           
    else:
        form = MenuItemForm()

    return render(request, 'admin/add_menu_items.html', {'form': form})


def customer_orders(request):
    # Your logic to fetch and display orders
    return render(request, 'orders.html')


def view_menu(request):
    # Fetch all menu items from the database
    menu_items = MenuItem.objects.all()  # You can filter or order the menu if needed
    return render(request, 'admin/view_menu.html', {'menu_items': menu_items})


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


def menu_item_list(request):
    menu_items = MenuItem.objects.all()  # Query to get all menu items
    return render(request, 'admin/menu_item_list.html', {'menu_items': menu_items})

def delete_menu_item(request, id):
    menu_item = get_object_or_404(MenuItem, id=id)

    if request.method == 'POST':
        menu_item.delete()
        return redirect('menu_item_list')  # Redirect to the menu item list after deletion

    return render(request, 'admin/delete_menu_item.html', {'menu_item': menu_item})





from django.shortcuts import render, get_object_or_404, redirect




# View to display all categories
def view_category(request):
    categories = Category.objects.all()  # Fetch all categories
    return render(request, 'admin/view_category.html', {'categories': categories})

# View to add a new category
def add_category(request):
    if request.method == 'POST':
        cname = request.POST.get('cname')
        status = request.POST.get('status') == 'on'
        if cname:
            Category.objects.create(cname=cname, status=status)
            messages.success(request, 'Category added successfully!')
            return redirect('view_category')
        else:
            messages.error(request, 'Category name is required.')
    return render(request, 'admin/add_category.html')

# View to edit an existing category
def edit_category(request, cid):
    category = get_object_or_404(Category, cid=cid)
    if request.method == 'POST':
        category.cname = request.POST.get('cname')
        category.status = request.POST.get('status') == 'on'
        if category.cname:
            category.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('view_category')
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

# View for adding a new subcategory
def add_subcategory(request):
    if request.method == 'POST':
        scname = request.POST.get('scname')
        cid = request.POST.get('cid')
        status = request.POST.get('status') == 'on'  # Checkbox value handling
        SubCategory.objects.create(scname=scname, cid_id=cid, status=status)
        messages.success(request, 'Subcategory added successfully.')
        return redirect('view_subcategory')
    
    categories = Category.objects.all()
    return render(request, 'admin/add_subcategory.html', {'categories': categories})

# View for editing a subcategory
def edit_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)

    if request.method == 'POST':
        subcategory.scname = request.POST.get('scname')
        subcategory.cid_id = request.POST.get('cid')
        subcategory.status = request.POST.get('status') == 'on'
        subcategory.save()
        messages.success(request, 'Subcategory updated successfully.')
        return redirect('view_subcategory')

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












