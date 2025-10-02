from rest_framework import serializers
from .models import Block, Room, Profile
from django.contrib.auth.models import User

class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ["id", "name", "description", "polygon", "floorplan_available"]

class RoomSerializer(serializers.ModelSerializer):
    block = BlockSerializer()
    class Meta:
        model = Room
        fields = ["room_code", "block", "floor", "name", "coordinates"]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
            extra_kwargs={"password": {"write_only": True}}
        )
        user.is_active = False  # User must verify email
        user.save()
        return user