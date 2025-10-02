from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from .models import Room, Block
from .serializer import RoomSerializer, RegisterSerializer, UserSerializer

verification_tokens = {}

@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = get_random_string(32)
        verification_tokens[token] = user.username

        verification_link = f"http://127.0.0.1:8000/api/verify-email/?token={token}/"
        send_mail(
            "Verify your UWE Class Locator account",
            f"Click the link to verify your email: {verification_link}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return Response({"message": "Check your uwe email to verify your account."}, status=201)
    return Response(serializer.errors, status=400)

@api_view(["GET"])
@permission_classes([AllowAny])
def verify_email(request, token):
    username = verification_tokens.get(token)
    if not username:
        return Response({"error": "Invalid or expired token"}, status=400)

    try:
        user = User.objects.get(username=username)
        user.is_active = True
        user.profile.email_verified = True
        user.profile.save()
        user.save()

        del verification_tokens[token]
        return Response({"message": "Email verified successfully."}, status=200)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None and user.is_active:
        login(request, user)
        return Response({"message: "Login successful"})
    return Response({"error": "Invalid credentials or unverified email"}, status=400)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

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

