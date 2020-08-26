from django.urls import path
from .views import *


urlpatterns = [
    # home-feed
    path('home-feed/', homeFeed, name='homeFeed'),

    # search
    path('search/<str:pattern>', searchUser, name='searchUser'), #returns all matching usernames for given pattern

    # myprofile posts OR  friend profile posts
    path('getuserposts/<str:username>', getUserPosts, name='getUserPosts'),  #returns single users posts

    # User
    path('user/login/', loginUser, name='loginUser'),
    path('user/logout/', logoutUser, name='logoutUser'),
    path('user/register/', registerUser, name='registerUser'),

    # Photopost
    path('photopost/create/', createPhotopost, name='createPhotopost'),
    path('photopost/delete/<str:pk>', deletePhotopost, name='deletePhotopost'),
    
    # likes of post
    path('like/<str:pk>', likePost, name='likePost'),
    path('getlikes/<str:pk>', getAllLikes, name='getAllLikes'),

    # comments of post
    path('comment/<str:pk>', commentPost, name='commentPost'),
    path('comment/delete/<str:pk>', deleteCommentPost, name='deleteCommentPost'),
    path('getcomments/<str:pk>', getAllComments, name='getAllComments'),

]