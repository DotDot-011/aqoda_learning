from GuestRecord import GuestRecord
from Guest import Guest

class Error(Exception):

    pass

class RoomNotFound(Error):
    
    def __init__(self, room_number: str) -> None:
        print(f"Don't have room {room_number}")

class CannotBook(Error):
    
    def __init__(self, room_number: str, guest: Guest, guest_record: GuestRecord) -> None:
        print(f"Cannot book room {room_number} for {guest.name}, The room is currently booked by {guest_record.guest.name}.")

class NoKeycardAvailable(Error):

    def __init__(self) -> None:
        print("No available keycard left")

class KeycardNotFound(Error):

    def __init__(self, keycard_number) -> None:
        print(f"Don't have keycard {keycard_number}")

class GuestNotFound(Error):

    def __init__(self, room_number: str) -> None:
        print(f"Room {room_number} has no guest")

class FloorNotFound(Error):

    def __init__(self, floor_number: str) -> None:
        print(f"Don't have floor {floor_number}")

class KeycardNotAssign(Error):
    
    def __init__(self) -> None:
        print("This keycard haven't yet assigned")

class CannotCheckout(Error):
    
    def __init__(self, guest_record: GuestRecord, keycard_number: str) -> None:
        print(f"Only {guest_record.guest.name} can checkout with keycard number {keycard_number}.")

class WrongSymbol(Error):
    
    def __init__(self) -> None:
        print("Not correct symbol")

class CannotBookAllFloor(Error):

    def __init__(self, floor_number: str, guest: Guest) -> None:
        print(f"Cannot book floor {floor_number} for {guest.name}.")