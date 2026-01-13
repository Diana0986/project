from django.db import models
from django.contrib.auth.models import \
    AbstractUser


class User(AbstractUser):
    image = models.ImageField(upload_to='users_image', blank=True, null=True)
    middle_name = models.CharField(max_length=100, blank=True)
    birthday = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    link_vk = models.URLField(max_length=200, blank=True)
    link_tg = models.URLField(max_length=200, blank=True)
    
    email = models.EmailField(unique=True, blank=False)
    
    class Meta:
        db_table = 'user'
    
    
    def __str__(self):
        return self.username
    