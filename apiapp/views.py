from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .serializers import registerUserSZR,loginUserSZR,createPhotopostSZR,getPhotopostSZR,getUsernamesSZR,postCommentSZR,getCommentSZR
from .models import Photopost,LikesPhotopost,CommentsPhotopost

#paginator 
PHOTOS_PER_PAGE = 5
SEARCH_RESULTS_PER_PAGE = 30
GETALLLIKES_PER_PAGE = 20
GETALLCOMMENTS_PER_PAGE = 20

# Register user
@api_view(['POST'])
def registerUser(request):
    szr = registerUserSZR(data=request.data)
    if szr.is_valid():
        new_user = User.objects.create_user(username=szr.data['username'],
                                            email=szr.data['email'],
                                            password=szr.data['password'])        
        if new_user:
            return Response({   'response':'success', 'message':'Registration completed. Please login'  })
    try:
        user = User.objects.get(username=szr.data['username']) 
        return Response({ 'response':'error', 'message':'username not available'})
    except:
        return Response({ 'response':'error', 'message':'invalid input'})
    return Response({ 'response':'error', 'message':'server error'})


# login user
@api_view(['POST'])
def loginUser(request):
    szr = loginUserSZR(data=request.data)
    if szr.is_valid():
        try:
            user = User.objects.get(username=szr.data['username']) 
            if user.check_password(szr.data['password']):
                return Response({ 'response':'success','token': Token.objects.get(user=user).key })
            else:
                return Response({'response':'error', 'message':'incorrect password' })
        except:
            return Response({ 'response':'error','message':'username doesnt exist' })
    return Response({'response':'error', 'message':'server error' })


# logout user
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def logoutUser(request):
    #Add delete token function here
    return Response({'response':'success','message':'logged out' })


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def homeFeed(request, pageNo):
    posts = Photopost.objects.all().order_by('-date_created') #change this to latest posts alone - 
    #Practically you need only need last 2 days posts (not one year before posts in feed)
    return getData(request,posts,pageNo)
    
# search user and retrive a list of matchin names
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def searchUser(request, pattern):
    matches = User.objects.filter(username__contains=pattern)
    page_obj = Paginator(matches,SEARCH_RESULTS_PER_PAGE)
    szr = getUsernamesSZR(page_obj.page(1),many=True)
    return Response(szr.data)

# my profile posts or friends profile posts
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def getUserPosts(request, username, pageNo):
    user = User.objects.get(username=username)
    posts = Photopost.objects.filter(uploaded_by=user).order_by('-date_created')    
    return getData(request,posts,pageNo)

def getData(request,posts,pageNo):
    final_data = []
    top_likes = []
    top_cmnts = []
    for i in posts:
        lks = LikesPhotopost.objects.filter(image=i).order_by('-date_created')
        cmnts = CommentsPhotopost.objects.filter(image=i).order_by('-date_created')
        top_likes = []
        top_cmnts = []

        # add latest 3 likes to top_likes
        count = 3
        for j in lks:
            if count > 0:
                top_likes.append({'username':j.by.username})
                count = count - 1
            else:
                break

        # add latest 3 comments to top_cmnts
        count = 3
        for j in cmnts:
            if count > 0:
                top_cmnts.append({'username':j.by.username, 'comment':j.comment})
                count = count - 1
            else:
                break
        
        try:
            LikesPhotopost.objects.get(image=i,by=request.user)
            is_liked = True
        except:
            is_liked = False
        httphdr = request.is_secure() and "https://" or "http://"
        final_data.append({
                'id':i.id,
                'image':i.image, # httphdr+request.get_host()+i.image.url - set this if its not working in localhost -(to return full URL so that UI running on other domains can display image)
                'uploaded_by':i.uploaded_by,
                'is_liked': is_liked,
                'hashtags':i.hashtags,
                'date_created':i.date_created,
                'topLikes':top_likes,
                'totalLikes':lks.__len__,
                'topComments':top_cmnts,
                'totalComments':cmnts.__len__,
                })
    page_obj = Paginator(final_data,PHOTOS_PER_PAGE)
    try:
        szr = getPhotopostSZR(page_obj.page(pageNo),many=True)
    except:
        return Response({'response':'error','message':'PageDoestNotExist'})
    return Response(szr.data)
       

# Photopost create
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def createPhotopost(request):
    newPost = Photopost(uploaded_by=request.user) 
    szr = createPhotopostSZR(newPost,data=request.data)
    if szr.is_valid():
        szr.save()
        return Response(szr.data)
    return Response({'response':'error'})


# Photopost delete
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def deletePhotopost(request, pk):
    post = Photopost.objects.get(id=pk)
    if request.user != post.uploaded_by:
        return Response({'response':'error','message': 'this post does not belong to you'})
    post.delete()
    return Response({'response':'success','message':'post deleted successfully'})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def likePost(request, pk):
    post = Photopost.objects.get(id=pk)
    try:
        newlike = LikesPhotopost(image=post,by=request.user)
        newlike.save()
    except:
        LikesPhotopost.objects.get(image=post,by=request.user).delete()
        return Response({'response':'success','message':'disliked'})
    return Response({'response':'success','message':'liked'})


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def getAllLikes(request, pk):
    post = Photopost.objects.get(id=pk)
    likes = LikesPhotopost.objects.filter(image=post).order_by('-date_created')
    usernames = []
    for i in likes:
        usernames.append({'username':i.by.username})
    page_obj = Paginator(usernames,GETALLLIKES_PER_PAGE)
    szr = getUsernamesSZR(page_obj.page(1),many=True)
    return Response(szr.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def commentPost(request, pk):
    szr = postCommentSZR(data=request.data)
    if szr.is_valid():
        post = Photopost.objects.get(id=pk)
        newCmnt = CommentsPhotopost(image=post,by=request.user,comment=szr.data['comment'])
        newCmnt.save()
        return Response({'response':'success','message':'comment posted successfully'})
    return Response({'response':'error'})


@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def deleteCommentPost(request, pk):
    cmnt = CommentsPhotopost.objects.get(id=pk)
    if request.user != cmnt.by:
        return Response({'response':'error','message':'this post does not belong to you'})
    cmnt.delete()
    return Response({'response':'success','message':'comment deleted successfully'})


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def getAllComments(request, pk):
    post = Photopost.objects.get(id=pk)
    cmnts = CommentsPhotopost.objects.filter(image=post).order_by('-date_created')
    data = []
    for i in cmnts:
        data.append({'id':i.id,'username':i.by.username , 'comment':i.comment, 'date_created':i.date_created})
    page_obj = Paginator(data,GETALLCOMMENTS_PER_PAGE)
    szr = getCommentSZR(page_obj.page(1),many=True)
    return Response(szr.data)
