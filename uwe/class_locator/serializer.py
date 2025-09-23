from rest_framework import serializers
from .models import Block, Room

class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ["id", "name", "description", "polygon", "floorplan_available"]

class RoomSerializer(serializers.ModelSerializer):
    block = BlockSerializer()
    class Meta:
        model = Room
        fields = ["room_code", "block", "floor", "name", "coordinates"]
