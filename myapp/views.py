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
            login_obj = Login.objects.get(email=email, password=password)
            user = login_obj.user

            # For regular users
            messages.success(request, f'Welcome, {user.name}!')
            return redirect('index')  # Redirect to user homepage

        except Login.DoesNotExist:
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


# views.py

def add_employee(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            # Save the email and password to the Login model
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            login = Login.objects.create(email=email, password=password)
            
            # Now save the employee with the associated login
            employee = form.save(commit=False)  # Delay saving Employee
            employee.login = login  # Associate login with employee
            employee.save()  # Save the employee instance
            
            return redirect('employee_success')  # Redirect after successful form submission
    else:
        form = EmployeeForm()
    
    return render(request, 'admin/add_employee.html', {'form': form})

def employee_success(request):
    return render(request, 'admin/employee_success.html')







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