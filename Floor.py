from Room import Room

class Floor:

    def __init__(self, floor_number: str) -> None:
        self.number = floor_number
        self.rooms = []
    
    def add_room(self, room: Room) -> None:
        self.rooms.append(room) 

    def list_booked_room(self) -> list:
        booked_rooms = list(filter(lambda room: room.is_booked(), self.rooms))

        return booked_rooms

    def list_guest_name(self) -> list: 
        
        booked_rooms = self.list_booked_room()
        guest_names = list(map(lambda room: room.guest.name, booked_rooms))
        
        return guest_names
