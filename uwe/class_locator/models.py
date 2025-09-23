from django.db import models

class Block(models.Model):
    name = models.CharField(max_length=6, unique=True)
    description = models.TextField()
    polygon = models.JSONField(blank=True, null=True)
    floorplan_available = models.BooleanField(default=False)

    def __str__(self):
        return f"Block {self.name}"

class Room(models.Model):
    room_code = models.CharField(max_length=10, unique=True)
    block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name="rooms")
    floor = models.IntegerField()
    name = models.CharField(max_length=100, blank=True)
    coordinates = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.room_code