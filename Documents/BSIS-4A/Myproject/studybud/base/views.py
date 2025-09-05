from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User
from .form import RoomForm
# Create your views here.
'''rooms=[{'id': 1, 'name': 'Room A'}, 
       {'id': 2, 'name': 'Room B'}, 
       {'id': 3, 'name': 'Room C'}]'''


def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)   # ✅ sets session properly
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form= UserCreationForm()
    
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form': form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    room_count = rooms.count()
    topics = Topic.objects.all()
    room_messages = Message.objects.filter(room__in=rooms).order_by('-created')[:5]  # recent 5

    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'room_messages': room_messages
    }
    return render(request, 'base/home.html', context)




def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    room_participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room': room, 'room_messages': room_messages, 'room_participants': room_participants}
    return render(request, 'base/room.html', context)


def createRoom(request):
    form= RoomForm()

    context={'form': form}
    if request.method=='POST':
        form= RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    
    room= Room.objects.get(id=pk)
    form= RoomForm(instance=room)
    if request.user != Room.objects.get(id=pk).host:
        return HttpResponse('You are not allowed here!!')
    context={'form': form}
    if request.method=='POST':
        form= RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'base/room_form.html', context) 

@login_required(login_url='login')
def deleteRoom(request, pk):
    obj = Room.objects.get(id=pk)
    if request.user != obj.host:
        return HttpResponse('You are not allowed here!!')
    if request.method == 'POST':
        obj.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': obj})

@login_required(login_url='login')
def deleteMessage(request, pk):
    obj = Message.objects.get(id=pk)
    if request.user != obj.user:
        return HttpResponse('You are not allowed here!!')
    if request.method == 'POST':
        obj.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': obj})