from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    # If the User is deleted this Task will also be delete (models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)   #Set to creating date

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['complete']     #Order data by [complete] var