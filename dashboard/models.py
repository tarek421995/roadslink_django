from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# author model
class Author(models.Model):
    author = models.OneToOneField(User, on_delete= models.CASCADE,blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='First Name')
    last_name = models.CharField(max_length=100, null=True, blank=True,verbose_name='Last Name')
    designation = models.CharField(max_length=10, null=True)
    author_image = models.ImageField(upload_to='author/',verbose_name='Author Profile Image',blank=True, null=True)
    auth_status = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name_plural = 'Author'
    

    def __str__(self):
        return self.first_name
