from django.shortcuts import render, redirect
from .models import Room,Topic
from .form import RoomForm
# Create your views here.
'''rooms=[{'id': 1, 'name': 'Room A'}, 
       {'id': 2, 'name': 'Room B'}, 
       {'id': 3, 'name': 'Room C'}]'''

def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)
    topics = Topic.objects.all()
    context = {'rooms': rooms, 'topics': topics}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    
            
    context = {'room': room}
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

def updateRoom(request, pk):
    room= Room.objects.get(id=pk)
    form= RoomForm(instance=room)
    context={'form': form}
    if request.method=='POST':
        form= RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'base/room_form.html', context) 

def deleteRoom(request, pk):
    obj = Room.objects.get(id=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': obj})
