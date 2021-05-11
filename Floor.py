from Room import Room

class Floor:

    def __init__(self, floor_number: str, room_count_per_floor: int) -> None:
        self.number = floor_number
        self.rooms = []

        for room in range(1,room_count_per_floor+1):
            room_number = str(room + (int(self.number) * 100)) 
            self.rooms.append(Room(floor_number, room_number))
    
    def list_booked_room(self) -> list:
        booked_rooms = list(filter(lambda room: room.is_booked(), self.rooms))

        return booked_rooms

    def list_guest_name(self) -> list: 
        booked_rooms = self.list_booked_room()
        guest_names = list(map(lambda room: room.guest.name, booked_rooms))
        
        return guest_names
