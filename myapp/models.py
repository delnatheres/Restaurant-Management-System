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




