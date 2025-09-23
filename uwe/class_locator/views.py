from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Room
from .serializers import RoomSerializer

@api_view(["GET"])
def lookup_room(request, code):
    try:
        room = Room.objects.get(room_code=code.upper())
        serializer = RoomSerializer(room)
        return Response(serializer.data)
    except Room.DoesNotExist:
        return Response({"error": "Room not found"}, status=404)

