from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User,auth  # Import User model for creating new users
from django.contrib import messages  # Import messages framework for displaying messages to the user
from django.contrib.auth import authenticate,login,logout #Handles user's credentials ,login,logout and authentications.
from django.contrib.auth.decorators import login_required #Handles accesibility of view.
from .models import *
from itertools import chain
import random


def home(request):
    return render(request,'home.html')

def about(request):
    return render(request,'about.html')

def register(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        fname=request.POST.get('first_name')
        lname=request.POST.get('last_name')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
       
         #check if password is same 
         
        if pass1 == pass2:
            if User.objects.filter(email=email).exists():   #check if email already registered
                messages.info(request,'email already exists!')
                return redirect('register')
            elif User.objects.filter(username=uname).exists():   # check if  same username exists 
                messages.info(request,'username already taken!!')
                return redirect('register')
            else:
                user = User.objects.create_user(username=uname,first_name=fname,last_name=lname, email=email, password=pass1)
                user.save()
                
                #log user in and redirect to settings page
                user_login = auth.authenticate(username=uname,password=pass1)
                auth.login(request,user_login)
                
                # create a profile object for the new user
                
                user_model=User.objects.get(username=uname)
                new_profile=Profile.objects.create(user=user_model,id_user=user_model.id)
                new_profile.save()
                return redirect('setting')
        else:
            messages.info(request,'password does not matched!!')
            return redirect('register')
        
            
    else:
        return render(request,'signup.html')  
            
#view for loginpage
def loginn(request):
    if request.method =='POST':
        uname=request.POST['username']
        pass1=request.POST['pass1']
        user = auth.authenticate(username=uname,password=pass1)
        if user is not None:
            auth.login(request,user)
            return redirect('index')
        else:
            messages.info(request,'credentials Invalid')
            return redirect('loginn')
    else:    
        return render(request,'loginn.html')



 #view for logoutpage

@login_required(login_url='loginn')
def logout(request):
    return redirect('home')

#view for index
@login_required(login_url='loginn')
def index(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        messages.error(request, "Profile does not exist! Please create a profile.")
        return redirect('loginn')  # Redirect to profile creation page

    
    
    ###TO update feed only following users######
    user_following_list = []
    feed = [] 
    
    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)
        
    # Include the current user in the feed
    user_following_list.append(request.user.username)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)
    
    feed_list = list(chain(*feed))

    ###########USER SUGGGESTIONS#####
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))
    
    
    return render(request, 'index.html', {'user_profile': user_profile, 'posts':feed_list, 'suggestions_username_profile_list': suggestions_username_profile_list[:4]})

#logic for settings
@login_required(login_url='loginn')
def setting(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        # Retrieve bio safely
        bio = request.POST.get('bio', user_profile.bio)  # Default to current bio if not provided
        location = request.POST.get('location', user_profile.location)
        # Check if an image is uploaded
        if request.FILES.get('image') is None:
            image = user_profile.profileimg  # Use existing image if no new file is uploaded
        else:
            image = request.FILES.get('image')  # Use the uploaded image

        # Update profile fields
        user_profile.profileimg = image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()

        # Redirect after saving
        return redirect('setting')

    # Render the settings page
    return render(request, 'settings.html', {'user_profile': user_profile})


####CREATE AND UPLOAD POST#########
@login_required(login_url='loginn')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        content = request.POST.get('content',None)  
        image = request.FILES.get('image_upload')
        caption = request.POST.get('caption', '')
        if not content and not image and not caption:
            messages.error(request, "Please provide at least one field to upload a post!")
            return redirect('upload')
        new_post = Post.objects.create(user=user, image=image,content=content, caption=caption)
        new_post.save()

        return redirect('index')
    else:
        return render(request,'upload.html')
    
    
########LIKEPOSTS#######################

@login_required(login_url='loginn')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    
    post = Post.objects.get(id=post_id)
    
    like_filter = LikePost.objects.filter(post_id=post_id,username=username)
    
    if not like_filter.exists():  # No like exists; add a like
        LikePost.objects.create(post_id=post_id, username=username)
        post.no_of_likes += 1
    else:  # Like exists; remove it
        like_filter.delete()
        if post.no_of_likes > 0:  # Prevent decrementing below 0
            post.no_of_likes -= 1

    # Save the updated post
    post.save()

    return redirect('index')


#########profile page##############
@login_required(login_url='loginn')
def profile(request, pk):
    try:
        # Get the user object based on the username (pk)
        user_object = User.objects.get(username=pk)
    except User.DoesNotExist:
        return HttpResponse("User not found", status=404)
    
    # Safely retrieve the profile object using get_object_or_404
    user_profile = get_object_or_404(Profile, user=user_object)
    
    # Filter posts made by this user
    user_posts = Post.objects.filter(user=user_object)
    user_post_length = user_posts.count()  
    
    follower = request.user.username
    user = pk
    
    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))


    # Prepare context data for rendering
    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, 'profile.html', context)


######FOLLOWERS#############
@login_required(login_url='loginn')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']
        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('index')
    
######SEARCH ################
@login_required(login_url='loginn')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})

######DELETE _POST###############

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Post

@login_required(login_url='loginn')
def delete_post(request, post_id):
    # Fetch the post
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)

    # Ensure only the owner can delete the post
        if post.user == request.user.username:
            post.delete()
            messages.success(request, "Post deleted successfully.")
        else:
            messages.error(request, "You are not authorized to delete this post.")

    return redirect('index')  # Redirect to the feed




from django.urls import reverse
from datetime import datetime

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from datetime import datetime
from .models import Comment, Post

def add_comment(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=pk)  # Fetch the post by UUID
        content = request.POST.get('content')  # Get comment content from form

        if content:
            # Create the comment and save it
            comment = Comment(
                post=post,
                user=request.user.username,
                content=content,
                created_at=datetime.now()
            )
            comment.save()  # Save the comment to the database
            return redirect(reverse('index'))  # Redirect after adding the comment
        else:
            print("Comment content cannot be empty")
            return redirect(reverse('index'))
    else:
        return redirect(reverse('index'))

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post_id = comment.post.id
    comment.delete()  # Delete the comment
    return redirect('index')  # Redirect back to the post detail page
