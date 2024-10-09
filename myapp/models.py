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
    
    

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    phone = models.CharField(max_length=10)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=True)
    joinedon = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(null=True, blank=True)   # Use EmailField for better validation
    password = models.CharField(max_length=150, null=True, blank=True) 
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)  # Image field
    
    def __str__(self):
        return self.name
    
    
    

class Reservation(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)  # Updated to use Customer
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField()

    def __str__(self):
        return f"Reservation {self.id} - {self.customer.name}"

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

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('served', 'Served'),
    ]
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name="orders")  # Updated to use Customer
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.customer.name} - {self.menu_item.name}"

class Feedback(models.Model):
    customer = models.CharField(max_length=100)  # Updated to use Customer
    comments = models.CharField(max_length=1000)
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"
        ordering = ['-created_at']

    def __str__(self):
        return f"Feedback from {self.customer.name} - Rating: {self.rating}"

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
    orders = models.ManyToManyField('Order', blank=True)  # Link orders with the dashboard
    reservations = models.ManyToManyField('Reservation', blank=True)  # Link reservations with the dashboard
    leave_requests = models.ManyToManyField('LeaveRequest', blank=True)

    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name}'s Dashboard"
    
    
    
    

class LeaveRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=50)  # Adjust the length as needed
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.BooleanField(default=False)  # You can change default as per your requirement

    def __str__(self):
        return f"Leave Request from {self.employee.first_name} {self.employee.last_name} - {self.leave_type}"
    
    
    
    
    
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s wishlist item: {self.menu_item.name}"