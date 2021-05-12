from typing import IO
from Hotel import Hotel
from Keycard import Keycard
from Room import Room
from Guest import Guest

file = open("input.txt","r")
lines = file.readlines()
file.close()

for line in lines:
    words = line.split("\n")[0].split(" ")
    command = words[0]
    parameters = words[1:] 

    if(command == "create_hotel"):
        floor_count = int(parameters[0])
        room_count_per_floor = int(parameters[1])

        hotel = Hotel(floor_count, room_count_per_floor)

        print(f"Hotel created with {floor_count} floor(s), {room_count_per_floor} room(s) per floor.")
    elif(command == "book"):
        room_number = parameters[0]
        guest_name = parameters[1]
        guest_age = int(parameters[2])
        
        guest = Guest(guest_name, guest_age)
        try:
            new_guest_record = hotel.book(room_number, guest)
        
            print(f"Room {new_guest_record.room.number} is booked by {new_guest_record.guest.name} with keycard number {new_guest_record.keycard.number}.") 
        except IOError as error_message:
            print(error_message)
    elif(command == "list_available_rooms"):
        available_rooms = hotel.list_available_room()
        available_room_numbers = list(map(lambda room: room.number, available_rooms))
        
        print(", ".join(available_room_numbers))
    elif(command == "checkout"):
        keycard_number = parameters[0]
        guest_name = parameters[1]

        try:
            checkouted_guest_record = hotel.checkout(keycard_number, guest_name)

            print(f"Room {checkouted_guest_record.room.number} is checkout.")
        except IOError as error_message:
            print(error_message)
    elif(command == "list_guest"):
        guests = hotel.list_guest()
        guest_names = list(map(lambda guest: guest.name, guests))

        print(", ".join(guest_names))
    elif(command == "get_guest_in_room"):
        room_number = parameters[0]

        try:
            guest = hotel.get_guest_by_room_number(room_number)
            
            print(guest.name)
        except IOError as error_message:
            print(error_message)
    elif(command == "list_guest_by_age"):
        comparison_symbol = parameters[0]
        age = int(parameters[1])

        try:
            guests = hotel.list_guest_by_age(comparison_symbol, age)
            guest_names = list(map(lambda guest: guest.name, guests))

            print(", ".join(guest_names))
        except IOError as error_message:
            print(error_message)
    elif(command == "list_guest_by_floor"):
        floor_number = parameters[0]

        try:
            guests = hotel.list_guest_by_floor_number(floor_number)
            guest_names = list(map(lambda guest: guest.name, guests))

            print(", ".join(guest_names))
        except IOError as error_message:
            print(error_message)
    elif(command == "checkout_guest_by_floor"):
        floor_number = parameters[0]

        try:
            checkouted_guest_records = hotel.checkout_by_floor_number(floor_number)
            room_numbers = list(map(lambda record: record.room.number, checkouted_guest_records))

            print(f"Room {', '.join(room_numbers)} are checkout.")
        except IOError as error_message:
            print(error_message)

    elif(command == "book_by_floor"):
        floor_number = parameters[0]
        guest_name = parameters[1]
        guest_age = int(parameters[2])  
        
        guest = Guest(guest_name, guest_age)
        
        try:
            new_guest_records = hotel.book_by_floor_number(floor_number, guest)
            booked_room_numbers = list(map(lambda record: record.room.number, new_guest_records))
            used_keycards_number = list(map(lambda record: record.keycard.number, new_guest_records))

            print(f"Room {', '.join(booked_room_numbers)} are booked with keycard number {', '.join(used_keycards_number)}")
        except IOError as error_message:
            print(error_message)
