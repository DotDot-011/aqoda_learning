from Guest import Guest

class Keycard:
    
    def __init__(self, keycard_number: str) -> None:
        self.number = keycard_number
        self.guest = None
        self.room_number = None

    def is_using(self) -> bool:
        return bool(self.guest)
    
    def assign(self, guest: Guest, room_number: str) -> None:
        self.guest = guest
        self.room_number = room_number
    
    def clear(self) -> None:
        self.guest = None
        self.room_number = None
        