from .thing import Thing

class Checklist:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.things: list[Thing] = []
    
    def get_thing(self, thing_number: int) -> Thing:
        return self.things[thing_number - 1]
    
    def add_thing(self, thing: Thing) -> None:
        self.things.append(thing)

    def insert_thing(self, thing: Thing, thing_number: int) -> None:
        self.things.insert(thing_number - 1, thing)

    def rename_thing(self, thing_number: int, new_sentence: str) -> None:
        self.get_thing(thing_number).sentence = new_sentence

    def is_valid_thing_number_str(self, thing_number: str) -> bool:
        return thing_number.isdigit() and 0 <= int(thing_number) - 1 < len(self.things)

    def remove_thing(self, thing_number: int) -> None:
        self.things.pop(thing_number - 1)

    def clear_checklist(self) -> None:
        self.things.clear()

    def check_thing(self, thing: Thing) -> None:
        thing.check()
    
    def uncheck_thing(self, thing: Thing) -> None:
        thing.uncheck()

    def _all_things_checked(self) -> bool:
        return bool(self.things) and all(thing.is_checked for thing in self.things)
    
    def __str__(self) -> str:
        return f"{self.name} ✅" if self._all_things_checked() else f"{self.name}"