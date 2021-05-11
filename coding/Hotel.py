# TODO: add specific type for input, output
from Floor import Floor
from Keycard import Keycard
from Room import Room
from Guest import Guest

class Hotel:
    
    def __init__(self, floor_count: int, room_count_per_floor: int) -> None: 
        self.room_count_per_floor = room_count_per_floor
        self.floors = []
        
        for floor_number in range(1, floor_count + 1):
            floor = Floor(str(floor_number))
            
            for room_number in range(1, room_count_per_floor + 1): 
                floor.add_room(Room(str(floor_number), str(floor_number * 100 + room_number)))
            self.floors.append(floor)
        
        self.keycards = [] 
        keycard_count = floor_count * room_count_per_floor

        for keycard_number in range(1, keycard_count + 1):
            self.keycards.append(Keycard(str(keycard_number)))
        
    def get_floor_by_floor_number(self, floor_number: str) -> Floor:
        floors = list(filter(lambda floor: floor.number == floor_number, self.floors))
        floor_is_exist = len(floors) != 0

        if(floor_is_exist):
            return floors[0]
        else:      
            return None
    
    def get_floor_number_by_room_number(self, room_number: str) -> str:
        return str(int(room_number) // 100)

    def get_floor_by_room_number(self, room_number: str) -> Floor:
        floor_number = self.get_floor_number_by_room_number(room_number)

        return self.get_floor_by_floor_number(floor_number)

    def get_keycard_by_keycard_number(self, keycard_number: str) -> Keycard:
        keycards = list(filter(lambda keycard: keycard.number == keycard_number, self.keycards))
        keycard_is_exist = len(keycards) != 0 

        if(keycard_is_exist):
            return  keycards[0]
        else:
            return None

    def get_available_keycard(self) -> Keycard:
        keycards = list(filter(lambda keycard: not keycard.is_using(), self.keycards))
        keycard_is_exist = len(keycards) != 0

        if(keycard_is_exist):
            return keycards[0]
        else:
            return None

    def get_keycard_by_room_number(self, room_number: str) -> Keycard:
        keycards = list(filter(lambda keycard: keycard.room_number == room_number, self.keycards))
        keycard_is_exist = len(keycards) != 0

        if(keycard_is_exist): 
            return keycards[0]
        else:
            return None

    def get_room_by_room_number(self, room_number: str) -> Room: 
        floor = self.get_floor_by_room_number(room_number)
        
        if(not floor):
            return None
        
        rooms = list(filter(lambda room: room.number == room_number, floor.rooms))
        room_is_exist = len(rooms) != 0

        if(not room_is_exist):
            return None
        return rooms[0]

    def book(self, room: Room, guest: Guest) -> Keycard:
        keycard = self.get_available_keycard()
      
        room.book(guest)            
        keycard.assign(guest, room.number)
        
        return keycard
 
    def list_available_room(self) -> list: 
        available_rooms = []

        for floor in self.floors:
            available_rooms.extend(list(filter(lambda room: not room.is_booked(), floor.rooms)))

        return available_rooms

    def list_booked_room(self) -> list:
        booked_rooms = []

        for floor in self.floors:
            booked_rooms.extend(list(filter(lambda room: room.is_booked(), floor.rooms)))

        return booked_rooms

    def checkout(self, keycard: Keycard) -> Room:
        room = self.get_room_by_room_number(keycard.room_number)
        
        keycard.clear()
        room.clear()

        return room

    def list_guest_name(self) -> list:
        booked_rooms = self.list_booked_room()
        guest_names = list(map(lambda room: room.guest.name, booked_rooms))

        return guest_names
    
    def list_guest_name_by_age(self, comparison_symbol: str, age: int) -> list:
        booked_rooms = self.list_booked_room()

        if(comparison_symbol == '<'):
            rooms = list(filter(lambda room: room.guest.age < age, booked_rooms))
            guest_names = list(map(lambda room: room.guest.name, rooms))
        elif(comparison_symbol == '>'):
            rooms = list(filter(lambda room: room.guest.age > age, booked_rooms))
            guest_names = list(map(lambda room: room.guest.name, rooms))
        elif(comparison_symbol == '>='):
            rooms = list(filter(lambda room: room.guest.age >= age, booked_rooms))
            guest_names = list(map(lambda room: room.guest_name, rooms))
        elif(comparison_symbol == '<='):
            rooms = list(filter(lambda room: room.guest.age <= age, booked_rooms))
            guest_names = list(map(lambda room: room.guest.name, rooms))
        elif(comparison_symbol == '!='):
            rooms = list(filter(lambda room: room.guest.age != age, booked_rooms))
            guest_names = list(map(lambda room: room.guest.name, rooms))
        elif(comparison_symbol == '='):
            rooms = list(filter(lambda room: room.guest.age == age, booked_rooms))
            guest_names = list(map(lambda room: room.guest.name, rooms))
        else:

            return None
        return guest_names

    def checkout_by_floor(self, floor: Floor) -> list:
        checkouted_rooms = [] 

        booked_rooms = list(filter(lambda room: room.is_booked(), floor.rooms))
        for room in booked_rooms:
            keycard = self.get_keycard_by_room_number(room.number)
            checkouted_room = self.checkout(keycard)

            checkouted_rooms.append(checkouted_room)

        return checkouted_rooms

    def book_by_rooms(self, rooms: list, guest: Guest) -> list:
        used_keycards = []
    
        for room in rooms:
            used_keycards.append(self.book(room, guest))
            
        return used_keycards
