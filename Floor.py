from Room import Room

class Floor:

    def __init__(self, floor_number: str, room_count_per_floor: int) -> None:
        self.number = floor_number
        self.rooms = []

        for room in range(1,room_count_per_floor+1):
            room_number = str(room + (int(self.number) * 100)) 
            self.rooms.append(Room(floor_number, room_number))
    