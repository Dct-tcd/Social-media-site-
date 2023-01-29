from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.models import User , auth
from django.contrib import messages
from .models import Profile , Post
from django.contrib.auth.decorators import login_required

@login_required(login_url='signin')

def index(request):
    User_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=User_object)
    
    posts = Post.objects.all() 
    return render(request , 'index.html' , {'user_profile':user_profile , 'posts':posts})

def signup (request):
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request , 'Email is taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request , 'username Taken')
                return redirect('signup')
            else :
                user = User.objects.create_user(username=username , email = email , password=password)
                user.save()
                # log user in and redirect to setting page
                
                user_login = auth.authenticate(username=username , password=password)
                auth.login(request , user_login)
                
                
                
                
                # create a profile object for new user
                user_model = User.objects.get(username=username)
                new_proile = Profile.objects.create(user=user_model , id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
                
        else :
            messages.info(request , 'Password not matching')
            return redirect ('signup')
                    
    else :
        return render (request , 'signup.html')
    
def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username , password=password)
        
        if user is not None:
            auth.login(request , user)
            return redirect('/')
        else :
            messages.info(request,'Credentials Invalid')
            return redirect('signin')
        
        # pass
    else :
        return render(request , 'signin.html')    

def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        
        if request.FILES.get('image') == None:

            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']
            user_profile.save()
            
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save() 

        if request.FILES.get('image') != None:

            image = request.FILES.get('image')  
            bio = request.POST['bio']
            location = request.POST['location']
      
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()   
            
              
    return render(request , 'setting.html' , { 'user_profile' : user_profile })

@login_required(login_url='signin')

def logout(request):
    auth.logout(request)
    return redirect('signin')


def likepost(request):
    pass
    





def upload(request):
    
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        
        new_post =Post.objects.create(user=user,image=image,caption=caption)
        new_post.save()
        return redirect('/')
    else :
        return redirect('/')
    return HttpResponse('<h1>Upload view</h1>')
