from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Room, Block
from .serializer import RoomSerializer

@api_view(["GET"])
def lookup_room(request, code):
    try:
        room = Room.objects.get(room_code=code.upper())
        serializer = RoomSerializer(room)
        return Response(serializer.data)
    except Room.DoesNotExist:
        block_letter = "".join([c for c in code if c.isalpha()][:1])  # "A"
        floor_digit = int(code[0]) if code[0].isdigit() else None

        block = Block.objects.filter(name=block_letter).first()

        if block:
            return Response({
                "room_code": code,
                "exists": False,
                "block": {
                    "name": block.name,
                    "description": block.description,
                },
                "floor": floor_digit,
                "message": f"Room not in database. Estimated location: Block {block.name}, Floor {floor_digit}."
            })
        else:
            return Response({
                "room_code": code,
                "exists": False,
                "error": "Block not recognized"
            }, status=404)

