from typing import List,IO, Union
from Keycard import Keycard
from Room import Room
from Guest import Guest
from GuestRecord import GuestRecord
from ErrorCase import CannotBook, CannotBookAllFloor, CannotCheckout, FloorNotFound, GuestNotFound, KeycardNotAssign, KeycardNotFound, NoKeycardAvailable, RoomNotFound, WrongSymbol

class Hotel:
    
    def __init__(self, floor_count: int, room_count_per_floor: int) -> None: 
        self.create_rooms(floor_count, room_count_per_floor)
        self.create_keycards(floor_count, room_count_per_floor) 
        self.guest_records = []

    def __generate_room_numbers(self, floor_count: int, room_count_per_floor: int) -> List[int]:
        temp_room_numbers = list(range(1, room_count_per_floor + 1))
        floor_numbers = list(range(1, floor_count + 1))
        room_numbers = [room_number + (floor_number * 100) for room_number in temp_room_numbers for floor_number in floor_numbers]
        
        return room_numbers

    def __generate_keycard_numbers(self, floor_count: int, room_count_per_floor: int) -> List[int]:
        keycard_count = floor_count * room_count_per_floor
        keycard_numbers = list(range(1, keycard_count + 1))

        return keycard_numbers

    def create_keycards(self, floor_count: int, room_count_per_floor: int) -> None:
        keycard_numbers = self.__generate_keycard_numbers(floor_count, room_count_per_floor)
        self.keycards = list(map(lambda keycard_number: Keycard(str(keycard_number)), keycard_numbers))    

    def create_rooms(self, floor_count: int, room_count_per_floor: int) -> None:
        room_numbers = self.__generate_room_numbers(floor_count, room_count_per_floor)
        self.rooms = list(map(lambda room_number: Room(str(room_number // 100), str(room_number)), room_numbers))

    def get_keycard_by_keycard_number(self, keycard_number: str) -> Keycard:
        keycards = list(filter(lambda keycard: keycard.number == keycard_number, self.keycards))
        
        if(not keycards):
            raise KeycardNotFound(keycard_number)

        return keycards[0]
        
    def get_available_keycard(self) -> Keycard:
        used_keycards = list(map(lambda record: record.keycard, self.guest_records))
        available_keycards = list(filter(lambda keycard: keycard not in used_keycards, self.keycards))
        
        if(not available_keycards):
            raise NoKeycardAvailable()

        return available_keycards[0]

    def get_room_by_room_number(self, room_number: str) -> Room: 
        rooms = list(filter(lambda room: room.number == room_number, self.rooms))
        
        if(not rooms):
            raise RoomNotFound(room_number)
            
        return rooms[0]

    def get_guest_by_room_number(self, room_number: str) -> Guest:
        room = self.get_room_by_room_number(room_number)
        guest_records = list(filter(lambda record: record.room == room, self.guest_records))
        
        if(not guest_records):
            raise GuestNotFound(room_number)
        
        return guest_records[0].guest
    
    def get_guest_record_by_room_number(self, room_number: str) -> Union[GuestRecord, None]:
        room = self.get_room_by_room_number(room_number)
        guest_records = list(filter(lambda record: record.room == room, self.guest_records))
        
        if(not guest_records):
            return None
            
        return guest_records[0]

    def get_guest_record_by_keycard_number(self, keycard_number: str) -> Union[GuestRecord, None]:
        keycard = self.get_keycard_by_keycard_number(keycard_number)
        guest_records = list(filter(lambda record: record.keycard == keycard, self.guest_records))    
        
        if(not guest_records):
            return None
        
        return guest_records[0]

    def list_room_by_floor_number(self, floor_number: str) -> List[Room]:
        rooms = list(filter(lambda room: room.floor_number == floor_number, self.rooms))
        
        if(not rooms):
            raise FloorNotFound(floor_number)
        
        return rooms

    def book(self, room_number: str, guest: Guest) -> GuestRecord:
        guest_record = self.get_guest_record_by_room_number(room_number)
        
        if(guest_record): 
            raise CannotBook(room_number, guest, guest_record)
        
        room = self.get_room_by_room_number(room_number)
        keycard = self.get_available_keycard()
        new_guest_record = GuestRecord(guest, room, keycard)
        self.guest_records.append(new_guest_record)
        
        return new_guest_record
 
    def list_available_room(self) -> List[Room]: 
        booked_rooms = list(map(lambda record: record.room, self.guest_records))
        available_rooms = list(filter(lambda room: room not in booked_rooms, self.rooms))

        return available_rooms

    def checkout(self, keycard_number: str, guest_name: str) -> GuestRecord:
        guest_record = self.get_guest_record_by_keycard_number(keycard_number)
        
        if(not guest_record):
            raise KeycardNotAssign()

        if(guest_record.guest.name != guest_name):
            raise CannotCheckout(guest_record, keycard_number)
        
        self.guest_records.remove(guest_record)

        return guest_record

    def list_guest(self) -> List[Guest]:
        return list(map(lambda record: record.guest, self.guest_records))
    
    def list_guest_by_age(self, comparison_symbol: str, age: int) -> List[Guest]:
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
            raise WrongSymbol()

        return guests

    def list_guest_by_floor_number(self, floor_number: str) -> List[Guest]:
        rooms = self.list_room_by_floor_number(floor_number)
        guest_records = list(filter(lambda record: record.room in rooms, self.guest_records))
        guests = list(map(lambda record: record.guest, guest_records))

        return guests

    def checkout_by_floor_number(self, floor_number: str) -> List[GuestRecord]:
        rooms = self.list_room_by_floor_number(floor_number)
        guest_records = list(filter(lambda record: record.room in rooms, self.guest_records))
        checkouted_guest_records = list(map(lambda record: self.checkout(record.keycard.number, record.guest.name), guest_records))

        return checkouted_guest_records

    def book_by_floor_number(self, floor_number: str, guest: Guest) -> List[GuestRecord]:
        rooms = self.list_room_by_floor_number(floor_number)
        guest_records = list(filter(lambda record: record.room in rooms, self.guest_records))
        
        if(guest_records):
            raise CannotBookAllFloor(floor_number, guest)

        new_guest_records = list(map(lambda room: self.book(room.number, guest), rooms))
            
        return new_guest_records
