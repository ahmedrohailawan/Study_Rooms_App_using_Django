from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from Home.models import Room,Topic,Message,User
from Home.forms import TopicForm,RoomForm,MyUserCreationForm,UserForm 
# Create your views here.

    
def index(request):
    if request.user.is_authenticated:
        loged_user = request.user
        loged_user.is_online = True
        loged_user.save()

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.all()
    room_list = Room.objects.filter(
        Q(topics__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) 
    )
    room_messages = Message.objects.filter(Q(room__name__icontains=q))
    room_count = room_list.count()
    context = {'topics':topics,'room_list':room_list,'room_count':room_count,'room_messages':room_messages}
    return render(request, 'Home/index.html',context)

def room_page(request,id):
    room = Room.objects.get(id=id)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.user.is_authenticated:
        if request.method == 'POST':
            message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')   
            )
            room.participants.add(request.user)
            return redirect('room_page',id= room.id)

    context = {'room':room,'room_messages':room_messages,'participants':participants}
    return render(request, 'Home/room_page.html',context)


def room_details(request,id):
    room = Room.objects.get(id=id)
    participants = room.participants.all()
    context = {'room':room,'participants':participants}
    return render(request, 'Home/room_details.html',context)



@login_required(login_url='/login')
def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            messages.success(request, "Room was created successfully")
            return redirect('/home')

    context = {'form':form}
    return render(request, 'Home/room_add.html',context)


@login_required(login_url='/login')
def create_topic(request):
    form = TopicForm()
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Topic was Added successfully")
            return redirect('/home')
    context = {'form':form}
    return render(request, 'Home/topic_add.html',context)





def signup_user(request):
    page = 'signup'
    form = MyUserCreationForm()
    if request.user.is_authenticated:
        messages.success(request, "you have already signup!")
        return redirect('/home')    
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request,user)
            messages.success(request, "Registeration Successful!")
            return redirect("/")
        else:
            messages.success(request, "There was error in signing up , try again...")  
            return redirect('/signup')
    return render(request, 'Home/login_signup.html',{'form':form ,'page':page})



def login_user(request):
    page = 'login'
    if request.user.is_authenticated:
        messages.success(request, "you have already login!")
        return redirect('/home')
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, "login Successfully!")
            return redirect("/")
        else:
            messages.success(request, "There was error in logging In , try again...")  
            return redirect('/login')
    context = {'page':page}
    return render(request, 'Home/login_signup.html',context)


@login_required(login_url='/login')
def logout_user(request):
    if request.user.is_authenticated:
        loged_user = request.user
        loged_user.is_online = False
        loged_user.save()
        logout(request)
        messages.success(request, "Logout sucessfully...") 
        return redirect("/home")
    else:
        messages.success(request, "You are not login...")  
        return redirect('/login')

def user_profile(request,id):
    user = User.objects.get(id=id)
    room_messages = user.message_set.all()
    room_list = user.room_set.all()
    context = {'room_list':room_list,'room_messages':room_messages,'user':user}
    return render(request, 'Home/user_profile.html',context)

@login_required(login_url='/login')
def my_profile(request):
    user = request.user
    room_messages = user.message_set.all()
    room_list = user.room_set.all()
    context = {'room_list':room_list,'room_messages':room_messages,'user':user}
    return render(request, 'Home/my_profile.html',context)


@login_required(login_url='/login')
def update_user_profile(request):
    user = request.user
    form = UserForm(instance = user)
    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES,instance = user)
        if form.is_valid:
            form.save()
            return redirect('profile',id= user.id)
    return render(request, 'Home/user_profile_update.html',{'form':form})

@login_required(login_url='/login')
def update_user_password(request):   
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/home')
        else:
            messages.success(request, 'There was a error in changing password!')
            return redirect('/update_user_password')  
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'Home/user_password.html',{'form':form})




@login_required(login_url='/login')
def update_room(request, room_id):
    room = Room.objects.get(id=room_id)
    form = RoomForm(request.POST or None,instance=room)

    if request.user !=room.host:
        return HttpResponse('you are not allowed here')
    if form.is_valid():
        form.save()
        messages.success(request, "Room has been updated sucessfully...")
        return redirect('room_details',id= room.id)
    return render(request,'Home/room_update.html',{'room':room,'form':form})


@login_required(login_url='/login')
def delete_room(request, room_id):
    room = Room.objects.get(id=room_id)
    if request.user !=room.host:
        return HttpResponse('you are not allowed here')
    if request.method == "POST":
        room.delete()
        messages.success(request, "Room has been deleted sucessfully...")
        return redirect('/home')
    return render(request,'Home/delete.html',{'room':room})

@login_required(login_url='/login')
def delete_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method == "POST":
        topic.delete()
        messages.success(request, "Topic has been deleted sucessfully...")
        return redirect('/home')
    return render(request,'Home/delete_by_super.html',{'topic':topic})


@login_required(login_url='/login')
def delete_message(request, id):
    
    message = Message.objects.get(id=id)
    if request.user != message.user:
        return HttpResponse('you are not allowed here')
    if request.method == "POST":
        message.delete()
        messages.success(request, "message has been deleted sucessfully...")
        return redirect('/home')
    return render(request,'Home/delete.html',{'message':message})







