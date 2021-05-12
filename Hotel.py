from typing import IO
from Keycard import Keycard
from Room import Room
from Guest import Guest
from GuestRecord import GuestRecord

class Hotel:
    
    def __init__(self, floor_count: int, room_count_per_floor: int) -> None: 
        self.create_rooms(floor_count, room_count_per_floor)
        self.create_keycards(floor_count, room_count_per_floor) 
        self.guest_records = []

    def create_keycards(self, floor_count: int, room_count_per_floor: int) -> None:
        self.keycards = []
        keycard_count = floor_count * room_count_per_floor

        for keycard_number in range(1, keycard_count + 1):
            self.keycards.append(Keycard(str(keycard_number)))

    def create_rooms(self, floor_count: int, room_count_per_floor: int) -> None:
        self.rooms = []

        for floor_number in range(1, floor_count + 1):
            for room_number in range(1, room_count_per_floor + 1):
                self.rooms.append(Room(str(floor_number), str(room_number + (int(floor_number) * 100))))

    def get_keycard_by_keycard_number(self, keycard_number: str) -> Keycard:
        keycards = list(filter(lambda keycard: keycard.number == keycard_number, self.keycards))

        if(keycards):
            return  keycards[0]
        else:
            return None

    def get_available_keycard(self) -> Keycard:
        used_keycards = list(map(lambda record: record.keycard, self.guest_records))
        available_keycards = list(filter(lambda keycard: keycard not in used_keycards, self.keycards))

        if(available_keycards):
            return available_keycards[0]
        else:
            return None

    def get_room_by_room_number(self, room_number: str) -> Room: 
        rooms = list(filter(lambda room: room.number == room_number, self.rooms))

        if(rooms):
            return rooms[0]

        return None

    def get_guest_by_room_number(self, room_number: str) -> Guest:
        room = self.get_room_by_room_number(room_number)

        if(not room):
            raise IOError("Don't have room {room_number}")
        
        guest_records = list(filter(lambda record: record.room == room, self.guest_records))
        
        if(not guest_records):
            raise IOError(f"Room {room_number} has no guest")
        
        return guest_records[0].guest
    
    def get_guest_record_by_room(self, room: Room) -> GuestRecord:
        guest_records = list(filter(lambda record: record.room == room, self.guest_records))
        
        if(guest_records):
            return guest_records[0]
        
        return None

    def get_guest_record_by_keycard(self, keycard: Keycard) -> GuestRecord:
        guest_records = list(filter(lambda record: record.keycard == keycard, self.guest_records))
        
        if(guest_records):
            return guest_records[0]
        
        return None

    def book(self, room_number: str, guest: Guest) -> Keycard:
        room = self.get_room_by_room_number(room_number)

        if(not room):
           raise IOError(f"Don't have room {room_number}")

        guest_record = self.get_guest_record_by_room(room)

        if(guest_record):
            raise IOError(f"Cannot book room {room_number} for {guest.name}, The room is currently booked by {guest_record.guest.name}.")
        
        keycard = self.get_available_keycard()
        new_guest_record = GuestRecord(guest, room, keycard)
        self.guest_records.append(new_guest_record)
        
        return new_guest_record
 
    def list_available_room(self) -> list: 
        booked_rooms = list(map(lambda record: record.room, self.guest_records))
        available_rooms = list(filter(lambda room: room not in booked_rooms, self.rooms))

        return available_rooms

    def checkout(self, keycard_number: str, guest_name: str) -> Room:
        keycard = self.get_keycard_by_keycard_number(keycard_number)

        if(not keycard):
            raise IOError(f"Don't have keycard {keycard_number}")

        guest_record = self.get_guest_record_by_keycard(keycard)

        if(not guest_record):
            raise IOError(f"This keycard haven't yet assigned")

        if(guest_record.guest.name != guest_name):
            raise IOError(f"Only {guest_record.guest.name} can checkout with keycard number {keycard_number}.")
        
        self.guest_records.remove(guest_record)

        return guest_record

    def list_guest(self) -> list:
        return list(map(lambda record: record.guest, self.guest_records))
    
    def list_guest_by_age(self, comparison_symbol: str, age: int) -> list:

        if(comparison_symbol == '<'):
            guest_records = list(filter(lambda record: record.guest.age < age, self.guest_records))
            guests = list(map(lambda record: record.guest, guest_records))
        elif(comparison_symbol == '>'):
            guest_records = list(filter(lambda record: record.guest.age > age, self.guest_records))
            guests = list(map(lambda record: record.guest, guest_records))
        elif(comparison_symbol == '>='):
            guest_records = list(filter(lambda record: record.guest.age >= age, self.guest_records))
            guests = list(map(lambda record: record.guest, guest_records))
        elif(comparison_symbol == '<='):
            guest_records = list(filter(lambda record: record.guest.age <= age, self.guest_records))
            guests = list(map(lambda record: record.guest, guest_records))
        elif(comparison_symbol == '!='):
            guest_records = list(filter(lambda record: record.guest.age != age, self.guest_records))
            guests = list(map(lambda record: record.guest, guest_records))
        elif(comparison_symbol == '='):
            guest_records = list(filter(lambda record: record.guest.age == age, self.guest_records))
            guests = list(map(lambda record: record.guest, guest_records))
        else:
            raise IOError("Not correct symbol")

        return guests

    def list_guest_by_floor_number(self, floor_number: str) -> list:
        rooms = list(filter(lambda room: room.floor_number == floor_number, self.rooms))

        if(not rooms):
            raise IOError(f"Don't have floor {floor_number}")
        
        guest_records = list(filter(lambda record: record.room in rooms, self.guest_records))
        guests = list(map(lambda record: record.guest, guest_records))

        return guests

    def checkout_by_floor_number(self, floor_number: str) -> list:
        rooms = list(filter(lambda room: room.floor_number == floor_number, self.rooms))

        if(not rooms):
            raise IOError(f"Don't have floor {floor_number}")
        
        guest_records = list(filter(lambda record: record.room.floor_number == floor_number, self.guest_records))
        checkouted_guest_records = list(map(lambda record: self.checkout(record.keycard.number, record.guest.name), guest_records))

        return checkouted_guest_records

    def book_by_floor_number(self, floor_number: str, guest: Guest) -> list:
        rooms = list(filter(lambda room: room.floor_number == floor_number, self.rooms))

        if(not rooms):
            raise IOError(f"Don't have floor {floor_number}")

        guest_records = list(filter(lambda record: record.room in rooms, self.guest_records))

        if(guest_records):
            raise IOError(f"Cannot book floor {floor_number} for {guest.name}.")

        new_guest_records = list(map(lambda room: self.book(room.number, guest), rooms))
            
        return new_guest_records
