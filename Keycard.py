from Guest import Guest

class Keycard:
    
    def __init__(self, keycard_number: str) -> None:
        self.number = keycard_number
        self.is_using = False
    
    def assign(self) -> None:
        self.is_using = True

    def clear(self) -> None:
        self.is_using = False
