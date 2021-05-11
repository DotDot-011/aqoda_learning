from Guest import Guest

class Room:

    def __init__(self, floor_number: str, room_number: str) -> None:
        self.floor_number = floor_number
        self.number = room_number
        self.is_booked = False

    def book(self) -> None:
        self.is_booked = True

    def clear(self) -> None:
        self.is_booked = False
