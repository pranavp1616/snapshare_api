from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Photopost(models.Model):
    image           =   models.ImageField(upload_to='images/')
    uploaded_by     =   models.ForeignKey(User,on_delete=models.CASCADE)
    hashtags        =   models.CharField(max_length=255)
    date_created    =   models.DateTimeField(auto_now_add=True, verbose_name="date published")
    def __str__(self):
        return str(self.id)


#whenever a new User is created/registered a new token is added to Token table
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class LikesPhotopost(models.Model):
    image = models.ForeignKey(Photopost,on_delete=models.CASCADE)
    by = models.ForeignKey(User,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    class Meta:
        unique_together = ('image','by') #only one like for a post by a user
    def __str__(self):
        return str(self.image.id)+str(self.by.id)


class CommentsPhotopost(models.Model):
    image = models.ForeignKey(Photopost,on_delete=models.CASCADE)
    by = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    def __str__(self):
        return str(self.image.id)+str(self.by.id)+self.comment
        