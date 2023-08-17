from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.
class Phone(models.Model):
    user=models.ForeignKey(User, on_delete=CASCADE )
    phone=models.CharField(max_length=12, default="")
    
    is_safe= models.BooleanField(default=True)
    contact_list=models.ManyToManyField(User,related_name="contacts",blank=True)

    def __str__(self):
        return f"{self.phone} of {self.user} is safe {self.is_safe}" 