from django.db import models

# from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True, unique=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    USERNAME_FIELD = 'email'        # Login with email
    REQUIRED_FIELDS = ['username']  # Required when creating a user via createsuperuser

    def __str__(self):
        return self.username
    


# Created model for the password reset
import uuid

class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_when = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset for {self.user.username} at {self.created_when}"







# A Room is going to be a child of Topic. 
# means A Topic can have multiple rooms, whereas a Room can only have one Topic

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name



# This is a Standalone One Model, it can have many childerns like Message Class

# A Room can only have one Topic
class Room(models.Model):

    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)

    name = models.CharField(max_length=200)  #Here null=False means the DB can't have an instance of this model without having this value
    description = models.TextField(null=True, blank=True)  # blank=True for (.save()) form submission without text in this field.

    participants = models.ManyToManyField(User, related_name='participants', blank=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-updated', '-created']   #'-'(descending order la arrange) means most recently added Room will stay on Top of the site.


    def __str__(self):
        return self.name
    

class Message(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()

    # file = models.FileField(upload_to='chat_uploads/', blank=True, null=True)  # 👈 add this

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

   

    def __str__(self):
        return self.body[0:40]




from django.template.defaultfilters import filesizeformat

class MessageFile(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='chat_uploads/')

    def get_size(self):
        return filesizeformat(self.file.size)