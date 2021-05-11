from Guest import Guest
from Room import Room
from Keycard import Keycard

class GuestRecord:

    def __init__(self, guest: Guest, room: Room, keycard: Keycard) -> None:
        self.guest = guest
        self.room = room
        self.keycard = keycard
