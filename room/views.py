from django.shortcuts import render, redirect
from .models import Room, Message,RoomUser
import random
import string
from django.contrib.auth.decorators import login_required

# Helper function to generate random room 

def generate_room_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# View for creating a new room
@login_required(login_url='loginn')
def CreateRoomView(request):
    if request.method == "POST":
        username = request.POST["username"]
        room_id = generate_room_id()
         
        # Create a new room with random room_id
        Room.objects.create(room_id=room_id)

        # Redirect to the created room
        return redirect("room", room_id=room_id, username=username)

    return render(request, "editor.html")

# View for joining an existing room

@login_required(login_url='loginn')
def JoinRoomView(request):
    if request.method == "POST":
        username = request.POST["username"]
        room_id = request.POST["room_id"]

        try:
            existing_room = Room.objects.get(room_id=room_id)
        except Room.DoesNotExist:
            return redirect('home')  # Handle room not found

        # Redirect to the existing room
        return redirect("room", room_id=room_id, username=username)

    return render(request, "editor.html")


@login_required(login_url='loginn')
def RoomView(request, room_id, username):
    room = Room.objects.get(room_id=room_id)
    visited_rooms = request.session.get('visited_rooms', [])
    
    if room_id not in visited_rooms:
        # If the user hasn't visited the room before, add this room to their session data
        visited_rooms.append(room_id)
        request.session['visited_rooms'] = visited_rooms
    messages = Message.objects.filter(room=room).order_by('created_at')

    context = {
        'room_name': room_id,
        'user': username,
        'messages': messages,
    }

    return render(request, 'room.html', context)



@login_required(login_url='loginn')
def user_dashboard(request):
    # Get all rooms the user has joined through the RoomUser model
    user_rooms = RoomUser.objects.filter(username=request.user.username)  # This is fine for username as CharField
    
    user_rooms_count = user_rooms.count()
    
    room_message = "No rooms joined yet" if user_rooms_count == 0 else f"{user_rooms_count} rooms joined"

    context = {
        'user_rooms': user_rooms,
        'user_rooms_count': user_rooms_count,
        'room_message': room_message,
    }

    return render(request, 'profile.html', context)


