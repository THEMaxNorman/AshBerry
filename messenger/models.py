from __future__ import unicode_literals



from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Massage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null = True, related_name='+')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, null = True, related_name = '+')
    text = models.TextField(blank = True)
    time = models.DateTimeField(auto_now_add=True, null=True)
    read = models.BooleanField(default = False)

class App(models.Model):
    name = models.CharField(blank= True, max_length= 45)
    description = models.TextField(blank= True)
    link = models.CharField(blank= True, max_length= 100)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    active = models.BooleanField(default=True)
from django.db import models
class Wish(models.Model):
    text = models.TextField(blank=True)


class memeDef(models.Model):
    name = models.CharField(max_length=255, blank=True)
    definition = models.TextField(blank = True)
    document = models.FileField(upload_to='images/')
    poster = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class artPiece(models.Model):
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank = True)
    document = models.FileField(upload_to= 'ArtImages/')
    poster = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
class song(models.Model):
    name = models.CharField(max_length=255, blank=True)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    document = models.FileField(upload_to='Music/%Y/%m/%d/')
    album = models.CharField(max_length=255, blank=True)


class store_item(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to='StoreImages/%Y/%m/%d/')
    description = models.TextField(blank=True)
    price = models.DecimalField(decimal_places=2,max_digits=10, blank=True)
class bug_report(models.Model):
    time = models.DateTimeField(auto_now_add=True, null=True)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.TextField(blank=True)
class blog_post(models.Model):
    time = models.DateTimeField(auto_now_add=True, null=True)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.TextField(blank=True)
    text = models.TextField(blank=True)

 # the profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #the installed apps is a string with every installed apps name (name corresponds to key in renderer)
    #seperated by a comma
    installed_apps = models.TextField(default= 'messenger;/mainMessages,gmail;https://gmail.com,calculator;/calc,contacts;/contacts,appstore;/appstore')
    background_image = models.TextField(default='default')
    isFounder = models.BooleanField(default=False)
    paypalEmail = models.EmailField(blank= True)




@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

