from Guest import Guest

class Room:

    def __init__(self, floor_number: str, room_number: str) -> None:
        self.guest = None
        self.floor_number = floor_number
        self.number = room_number

    def is_booked(self) -> bool:
        return bool(self.guest)

    def book(self, guest: Guest) -> None:
        self.guest = guest

    def clear(self) -> None:
        self.guest = None
        