from django.db import models

class Login(models.Model):
    email = models.EmailField(null=True, blank=True) 
    password = models.CharField(max_length=255, default="")
    reset_token = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.email
    
    
    
    
class SignIn(models.Model):
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100,default="")
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # Note: In practice, you should never store passwords in plaintext
    status = models.BooleanField(default=True)  # True for active users, False for inactive users
    role=models.CharField(max_length=255,default="")
    def __str__(self):
        return f"{self.name} - {self.email}"   
    
    
from django.db import models

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=15)
    place = models.CharField(max_length=50, default='Unknown')
    phone = models.CharField(max_length=10)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=True)
    joinedon = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(null=True, blank=True)  # Use EmailField for better validation
    password = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"




class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('veg', 'Vegetarian'),
        ('non-veg', 'Non-Vegetarian'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='veg')  # New field

    def __str__(self):
        return self.name
    
    


class Category(models.Model):
    cid = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=10, null=False)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.cname

class SubCategory(models.Model):
    id = models.AutoField(primary_key=True)
    cid = models.ForeignKey(Category, on_delete=models.CASCADE)
    scname = models.CharField(max_length=10, null=False)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.scname
    


class Feedback(models.Model):
    customer = models.CharField(max_length=100, default='')
    customer_name = models.CharField(max_length=100)  # Storing the customer name directly
    comments = models.CharField(max_length=1000)
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"
        ordering = ['-created_at']

    def __str__(self):
        return f"Feedback from {self.customer_name} - Rating: {self.rating}"


class Customer(models.Model):
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class User(models.Model):  # This class is removed as per your request
    name = models.CharField(max_length=150, unique=True)
    place = models.CharField(max_length=255)
    login = models.OneToOneField(Login, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class EmployeeDashboard(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    leave_requests = models.ManyToManyField('LeaveRequest', blank=True)

    def __str__(self):
        return f"{self.employee.name}'s Dashboard"
    
    
    

class LeaveRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=50)  # Adjust the length as needed
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending') 

    def __str__(self):
        return f"Leave Request from {self.employee.name} - {self.leave_type}"
    
    
    
    
class Cart(models.Model):
    customer = models.ForeignKey('SignIn', on_delete=models.CASCADE)  # Link to SignIn model
    menu_item = models.ForeignKey('MenuItem', on_delete=models.CASCADE)  # Link to MenuItem model
    quantity = models.PositiveIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('customer', 'menu_item')  # Prevent duplicates for the same customer and menu item

    def __str__(self):
        return f"{self.quantity} of {self.menu_item.name} in cart"

    def get_total_price(self):
        return self.quantity * self.menu_item.price  # Calculate the total price for the items in cart
    
    
    


class Order(models.Model):
    PAYMENT_CHOICES = (
        ('cod', 'Cash on Delivery'),
        ('online', 'Online Payment'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('ready', 'Ready'),
    )

    customer = models.ForeignKey('SignIn', on_delete=models.CASCADE)  # Link to SignIn model for customers
    name = models.CharField(max_length=255)
    place = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=20, default="0000000000")  
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    menu_item = models.ForeignKey('MenuItem', on_delete=models.CASCADE)  # Link to MenuItem model
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.menu_item.name} (x{self.quantity})"
    
    
    
    from django.db import models

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)  # Link to Order model
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Total amount paid
    razorpay_payment_id = models.CharField(max_length=255, unique=True)  # Razorpay payment ID
    status = models.CharField(max_length=20, default='pending')  # Payment status (pending, successful, failed)
    created_at = models.DateTimeField(auto_now_add=True)  # Date and time of payment creation
    updated_at = models.DateTimeField(auto_now=True)  # Date and time of last update

    def __str__(self):
        return f'Payment of {self.amount} for Order {self.order.id} - Status: {self.status}'




from django.db import models

class TableReservation(models.Model):
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    number_of_guests = models.PositiveIntegerField()
    special_requests = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.customer_name} - {self.reservation_date} at {self.reservation_time}"




from django.db import models

class Reservation(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]
    
    customer_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    number_of_guests = models.PositiveIntegerField()
    special_requests = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")

    def __str__(self):
        return f"{self.customer_name} - {self.reservation_date}"






class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.menu_item.price * self.quantity
