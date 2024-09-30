from django.db import models

class Login(models.Model):
    email = models.EmailField(unique=True,default="")
    password = models.CharField(max_length=255,default="")
    reset_token = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return self.email

class User(models.Model):
    
    name = models.CharField(max_length=150, unique=True)
    place = models.CharField(max_length=255)
    login = models.OneToOneField(Login, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    
    
# page1/models.py

class SignIn(models.Model):
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # Note: In practice, you should never store passwords in plaintext
    status = models.BooleanField(default=True)  # True for active users, False for inactive users
    
    def __str__(self):
        return f"{self.name} - {self.email}"
    
    
    

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    phone = models.CharField(max_length=10)
    joinedon = models.DateTimeField(auto_now_add=True)
    login = models.OneToOneField(Login, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"




from django.contrib.auth.models import User

# Model for Menu Item
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name



# Model for Customer Reservations
class Reservation(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField()

    def __str__(self):
        return f"Reservation {self.id} - {self.customer.username}"

# Model for Customer Feedback
class Feedback(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.TextField()
    rating = models.PositiveIntegerField(default=5)  # Rating from 1-5
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.customer.username}"



class Category(models.Model):
    cid = models.AutoField(primary_key=True)  # Auto-incremented ID for category
    cname = models.CharField(max_length=10, null=False)  # Category name
    status = models.BooleanField(default=True)  # Status of category (True/False)

    def __str__(self):
        return self.cname  # Show the category name in admin panel




class Category(models.Model):
    cid = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=10, null=False)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.cname


class SubCategory(models.Model):
    id = models.AutoField(primary_key=True)
    cid = models.ForeignKey(Category, on_delete=models.CASCADE)  # Foreign Key to Category
    scname = models.CharField(max_length=10, null=False)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.scname
    
    
    
    # Model for Customer Orders
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default="Pending")  # Pending, Preparing, Delivered
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.menu_item.name}"
    
    
    
    
    
    