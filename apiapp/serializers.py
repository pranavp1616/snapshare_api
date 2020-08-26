from rest_framework import serializers
from .models import Photopost,LikesPhotopost
from django.contrib.auth.models import User

# register User
class registerUserSZR(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password']


# login User 
class loginUserSZR(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class createPhotopostSZR(serializers.ModelSerializer):
    class Meta:
        model = Photopost
        fields = ['image','hashtags']


class getPhotopostSZR(serializers.Serializer):
    id              =   serializers.IntegerField()
#    image           =   serializers.ImageField()
    image           =   serializers.CharField(max_length=2083) #we are returning image url (not image) 
    uploaded_by     =   serializers.CharField(max_length=255)
    is_liked        =   serializers.BooleanField(default=False)
    hashtags        =   serializers.CharField(max_length=255)
    date_created    =   serializers.DateTimeField(format="%d/%m/%Y at %I:%M %p")
    topLikes        =   serializers.ListField(child=serializers.CharField(max_length=255))
    topComments     =   serializers.ListField(child=serializers.CharField(max_length=255))


#search user serializer
class getUsernamesSZR(serializers.Serializer):
    username = serializers.CharField(max_length=255)


class postCommentSZR(serializers.Serializer):
    comment = serializers.CharField(max_length=255)


class getCommentSZR(serializers.Serializer):
    id       =   serializers.IntegerField()
    username =  serializers.CharField(max_length=255) 
    comment =   serializers.CharField(max_length=255)
    date_created    =   serializers.DateTimeField(format="%d/%m/%Y at %I:%M %p")

