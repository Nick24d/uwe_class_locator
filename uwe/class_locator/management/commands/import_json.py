import json
from django.core.management.base import BaseCommand
from class_locator.models import Block, Room

class Command(BaseCommand):
    help = "Import blocks and rooms from a JSON file"

    def add_arguments(self, parser):
        parser.add_argument("json_file", type=str, help="Path to the JSON file")

    def handle(self, *args, **kwargs):
        json_file = kwargs["json_file"]

        with open(json_file, "r", encoding="utf-8") as f:
            data = rooms.json


        for block_data in data:
            block, created = Block.objects.get_or_create(
                name=block_data["block"],
                defaults={"description": block_data.get("description", "")}
            )

            for room_code in block_data.get("rooms", []):
                Room.objects.get_or_create(
                    room_code=room_code,
                    block=block,
                    floor=int(room_code[0]) if room_code[0].isdigit() else 0,
                    defaults={"name": ""}
                )

        self.stdout.write(self.style.SUCCESS("JSON data imported successfully!"))
