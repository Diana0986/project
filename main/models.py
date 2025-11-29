from django.db import models
from django.utils.text import slugify

class Events(models.Model):
    img = models.ImageField(upload_to='events/images/')
    order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Event {self.order}"

class Clubs(models.Model):
    img = models.ImageField(upload_to='clubs/images/')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Club {self.id}"

class Services(models.Model):
    img = models.ImageField(upload_to='services/images/')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Service {self.id}"

class Support(models.Model):
    img = models.ImageField(upload_to='support/images/')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Support {self.id}"

class News(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    main_image = models.ImageField(upload_to='news/main/')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:7]
        super().save(*args, **kwargs)

    
    def __str__(self):
        return self.name
    

class NewsImage(models.Model):
    product = models.ForeignKey(News, on_delete=models.CASCADE, 
                                related_name='images')
    image = models.ImageField(upload_to='news/extra/')