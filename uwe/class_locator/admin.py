from django.contrib import admin
from .models import Block, Room

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "floorplan_available")
    search_fields = ("name",)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("room_code", "block", "floor", "name")
    list_filter = ("block", "floor")
    search_fields = ("room_code", "name")

