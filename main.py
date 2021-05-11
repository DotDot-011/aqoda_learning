# TODO: make new class -> GuestRecord, ContactRecord, Catalog, GuestInformation
from Hotel import Hotel
from Floor import Floor
from Keycard import Keycard
from Room import Room
from Guest import Guest

file = open("input.txt","r")
lines = file.readlines()
file.close()

def book_by_floor_number(hotel: Hotel, floor_number: str, guest: Guest) -> str:
    floor = hotel.get_floor_by_floor_number(floor_number)
    
    if(not floor):
        return "Don't have this floor"
    booked_rooms = floor.list_booked_room()
    booked_room_exist = len(booked_rooms) != 0

    if(booked_room_exist):
        return f"Cannot book floor {floor_number} for {guest_name}."
    else: # TODO: don't have to use
        used_keycards = hotel.book_by_rooms(floor.rooms, guest)
        booked_room_numbers = list(map(lambda keycard: keycard.room_number, used_keycards))
        used_keycards_number = list(map(lambda keycard: keycard.number, used_keycards))
        
        return f"Room {', '.join(booked_room_numbers)} are booked with keycard number {', '.join(used_keycards_number)}"


def checkout_by_floor_number(hotel: Hotel, floor_number: str) -> str:
    floor = hotel.get_floor_by_floor_number(floor_number) # TODO: learn try catch

    if(floor): 
        checkouted_rooms = hotel.checkout_by_floor(floor)
        room_numbers = list(map(lambda room: room.number, checkouted_rooms))
        
        return f"Room {', '.join(room_numbers)} are checkout."
    else:
        return f"Don't have floor {floor_number}" 

def checkout_by_keycard_number(hotel: Hotel, keycard_number: str, guest_name: str) -> str:
    keycard = hotel.get_keycard_by_keycard_number(keycard_number)

    if(not keycard): # TODO: learn try catch
        return f"Don't have keycard {keycard_number}" # TODO: make space between line
    if(keycard.guest.name  != guest_name): # TODO: 2 space -> 1 space
        return f"Only {guest_name} can checkout with keycard number {keycard_number}."
    else: # TODO: don't have to use
        room = hotel.checkout(keycard)

        return f"Room {room.number} is checkout."
        
def book_by_room_number(hotel: Hotel, room_number: str, guest: Guest) -> str:
    room = hotel.get_room_by_room_number(room_number)
    
    if(not room): # TODO: learn try catch
        return f"Don't have room {room_number}"
    if(room.is_booked()):
        return f"Cannot book room {room_number} for {guest.name}, The room is currently booked by {room.guest.name}."
    else: # TODO: don't have to use
        used_keycard = hotel.book(room, guest)

        print(f"Room {room_number} is booked by {guest.name} with keycard number {used_keycard.number}.") # TODO: change print -> return 

def list_available_room_number(hotel: Hotel) -> list: # TODO: don't have to use
    available_rooms = hotel.list_available_room()

    return list(map(lambda room: room.number, available_rooms))
 
for line in lines:
    words = line.split("\n")[0].split(" ")
    command = words[0]
    parameter = words[1:] # TODO: make space between line
    if(command == "create_hotel"):
        floor_count = int(parameter[0])
        room_count_per_floor = int(parameter[1])

        hotel = Hotel(floor_count, room_count_per_floor)

        print(f"Hotel created with {floor_count} floor(s), {room_count_per_floor} room(s) per floor.")
    elif(command == "book"):
        room_number = parameter[0]
        guest_name = parameter[1]
        guest_age = int(parameter[2])

        guest = Guest(guest_name, guest_age)

        print(book_by_room_number(hotel, room_number, guest))
    elif(command == "list_available_rooms"):
        print(", ".join(list_available_room_number(hotel)))
    elif(command == "checkout"):
        keycard_number = parameter[0]
        guest_name = parameter[1]

        print(checkout_by_keycard_number(hotel, keycard_number, guest_name))
    elif(command == "list_guest"):
        print(", ".join(hotel.list_guest_name()))
    elif(command == "get_guest_in_room"):
        room_number = parameter[0]

        room = hotel.get_room_by_room_number(room_number)

        if(room):
            print(room.guest.name)
        else:
            print(f"Don't have room {room_number}")
    elif(command == "list_guest_by_age"):
        comparison_symbol = parameter[0]
        age = int(parameter[1])

        guest_names = hotel.list_guest_name_by_age(comparison_symbol, age)

        if(guest_names):
            print(", ".join(guest_names))
        else:
            print("Not correct symbol")
    elif(command == "list_guest_by_floor"):
        floor_number = parameter[0]

        floor = hotel.get_floor_by_floor_number(floor_number)

        if(floor):
            print(", ".join(floor.list_guest_name()))
        else:
            print(f"Don't have floor {floor_number}")
        
    elif(command == "checkout_guest_by_floor"):
        floor_number = parameter[0]

        print(checkout_by_floor_number(hotel, floor_number))

    elif(command == "book_by_floor"):
        floor_number = parameter[0]
        guest_name = parameter[1]
        guest_age = int(parameter[2])  
        
        guest = Guest(guest_name, guest_age)
        
        print(book_by_floor_number(hotel, floor_number, Guest))
