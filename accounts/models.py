from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class CustomUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=11)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=10)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return self.user.username


