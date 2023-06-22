from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Catogery(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.name) + '  ' + str(self.id)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_per_user_field')
        ]

class Link(models.Model):
    name = models.ForeignKey(Catogery, on_delete=models.CASCADE)
    product_link = models.URLField()
    collection = models.BooleanField(default=1)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.id)
    

class Collected_data(models.Model):
    name = models.ForeignKey(Link, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000, blank=True)
    rating = models.CharField(max_length=1000, blank=True)
    review = models.CharField(max_length=1000, blank=True)
    isAvaliable = models.CharField(max_length=1000, blank=True)
    price = models.CharField(max_length=1000, blank=True)
    mrp = models.CharField(max_length=1000, blank=True)
    seller = models.CharField(max_length=1000, blank=True)
    ASIN = models.CharField(max_length=1000, blank=True)
    First_date = models.CharField(max_length=1000, blank=True)
    created = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.name) + str(self.created)
    
    class Meta:
        ordering = ['-created']

