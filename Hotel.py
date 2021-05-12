from typing import IO
from Floor import Floor
from Keycard import Keycard
from Room import Room
from Guest import Guest
from GuestRecord import GuestRecord

class Hotel:
    
    def __init__(self, floor_count: int, room_count_per_floor: int) -> None: 
        self.floors = []
        
        for floor_number in range(1, floor_count + 1):
            self.floors.append(Floor(str(floor_number), room_count_per_floor))
        
        self.keycards = [] 
        keycard_count = floor_count * room_count_per_floor

        for keycard_number in range(1, keycard_count + 1):
            self.keycards.append(Keycard(str(keycard_number)))

        self.guest_records = []

    def get_floor_by_floor_number(self, floor_number: str) -> Floor:
        floors = list(filter(lambda floor: floor.number == floor_number, self.floors))

        if(floors):
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

        if(keycards):
            return  keycards[0]
        else:
            return None

    def get_available_keycard(self) -> Keycard:
        keycards = list(filter(lambda keycard: not keycard.is_using, self.keycards))

        if(keycards):
            return keycards[0]
        else:
            return None

    def get_keycard_by_room_number(self, room_number: str) -> Keycard:
        keycards = list(filter(lambda keycard: keycard.room_number == room_number, self.keycards))

        if(keycards): 
            return keycards[0]
        else:
            return None

    def get_room_by_room_number(self, room_number: str) -> Room: 
        floor = self.get_floor_by_room_number(room_number)
        
        if(not floor):
            return None
        
        rooms = list(filter(lambda room: room.number == room_number, floor.rooms))
        room_is_exist = len(rooms) != 0

        if(not rooms):
            return None

        return rooms[0]

    def get_guest_by_room_number(self, room_number: str) -> Guest:
        room = self.get_room_by_room_number(room_number)

        if(not room):
            raise IOError("Don't have room {room_number}")
        
        records = list(filter(lambda record: record.room == room, self.guest_records))
        
        if(not records):
            raise IOError(f"Room {room_number} has no guest")
        
        return records[0].guest

    def book(self, room_number: str, guest: Guest) -> Keycard:
        room = self.get_room_by_room_number(room_number)

        if(not room):
           raise IOError(f"Don't have room {room_number}")

        records = list(filter(lambda record: record.room == room, self.guest_records))

        if(records):
            raise IOError(f"Cannot book room {room_number} for {guest.name}, The room is currently booked by {records[0].guest.name}.")
        
        keycard = self.get_available_keycard()
        keycard.assign()
        record = GuestRecord(guest, room, keycard)
        self.guest_records.append(record)
        
        return record
 
    def list_available_room(self) -> list: 
        available_rooms = []

        booked_rooms = list(map(lambda record: record.room, self.guest_records))

        for floor in self.floors:
            available_rooms.extend(list(filter(lambda room: room not in booked_rooms, floor.rooms)))

        return available_rooms

    def checkout(self, keycard_number: str, guest_name: str) -> Room:
        keycard = self.get_keycard_by_keycard_number(keycard_number)

        if(not keycard):
            raise IOError(f"Don't have keycard {keycard_number}")

        records = list(filter(lambda record: record.keycard == keycard, self.guest_records))

        if(not records):
            raise IOError(f"This keycard haven't yet assigned")

        record = records[0]
        
        if(record.guest.name != guest_name):
            raise IOError(f"Only {record.guest.name} can checkout with keycard number {keycard_number}.")
        
        room = record.room

        keycard.clear()
        self.guest_records.remove(record)

        return room

    def list_guest_name(self) -> list:
        return list(map(lambda record: record.guest.name, self.guest_records))
    
    def list_guest_name_by_age(self, comparison_symbol: str, age: int) -> list:

        if(comparison_symbol == '<'):
            records = list(filter(lambda record: record.guest.age < age, self.guest_records))
            guest_names = list(map(lambda record: record.guest.name, records))
        elif(comparison_symbol == '>'):
            records = list(filter(lambda record: record.guest.age > age, self.guest_records))
            guest_names = list(map(lambda record: record.guest.name, records))
        elif(comparison_symbol == '>='):
            records = list(filter(lambda record: record.guest.age >= age, self.guest_records))
            guest_names = list(map(lambda record: record.guest_name, records))
        elif(comparison_symbol == '<='):
            records = list(filter(lambda record: record.guest.age <= age, self.guest_records))
            guest_names = list(map(lambda record: record.guest.name, records))
        elif(comparison_symbol == '!='):
            records = list(filter(lambda record: record.guest.age != age, self.guest_records))
            guest_names = list(map(lambda record: record.guest.name, records))
        elif(comparison_symbol == '='):
            records = list(filter(lambda record: record.guest.age == age, self.guest_records))
            guest_names = list(map(lambda record: record.guest.name, records))
        else:
            raise IOError("Not correct symbol")

        return guest_names

    def list_guest_by_floor_number(self, floor_number: str) -> list:
        floor = self.get_floor_by_floor_number(floor_number)

        if(not floor):
            raise IOError(f"Don't have floor {floor_number}")
        
        records = list(filter(lambda record: record.room.floor_number == floor_number, self.guest_records))
        guests = list(map(lambda record: record.guest, records))

        return guests

    def checkout_by_floor_number(self, floor_number: str) -> list:
        floor = self.get_floor_by_floor_number(floor_number)

        if(not floor):
            raise IOError(f"Don't have floor {floor_number}")
        
        records = list(filter(lambda record: record.room.floor_number == floor_number, self.guest_records))
        checkouted_rooms = list(map(lambda record: self.checkout(record.keycard.number, record.guest.name), records))

        return checkouted_rooms

    def book_by_floor_number(self, floor_number: str, guest: Guest) -> list:
        floor = self.get_floor_by_floor_number(floor_number)

        if(not floor):
            raise IOError(f"Don't have floor {floor_number}")

        records_in_floor = list(filter(lambda record: record.room.floor_number == floor_number, self.guest_records))

        if(records_in_floor):
            raise IOError(f"Cannot book floor {floor_number} for {guest.name}.")

        available_rooms = self.list_available_room()
        available_rooms_in_floor = list(filter(lambda room: room.floor_number == floor_number, available_rooms))
        records = list(map(lambda room: self.book(room.number, guest), available_rooms_in_floor))
            
        return records
