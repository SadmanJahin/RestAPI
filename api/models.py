from django.db import models

# Create your models here.


class Task(models.Model):
    title=models.CharField(max_length=200)
    completed=models.BooleanField(default=False,blank=True,null=True)
    
    
    def __str__(self):
        return self.title
    
    
    
class File(models.Model):
    title = models.CharField(max_length=150)
    file=models.FileField(upload_to='documents',max_length=100,blank=False)
    
    
    def __str__(self):
        return self.title