from .thing import Thing


class Checklist:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.things: list[Thing] = []

    def get_thing(self, thing_number: int) -> Thing:
        return self.things[thing_number - 1]

    def add_thing(self, thing: Thing) -> None:
        self.things.append(thing)

    def insert_thing(self, thing_number: int, thing: Thing) -> None:
        self.things.insert(thing_number - 1, thing)

    def rename_thing(self, thing_number: int, new_sentence: str) -> None:
        self.get_thing(thing_number).text = new_sentence

    def reposition_thing(self, thing_number: int, insertion_position: int) -> None:
        thing: Thing = self.remove_thing(thing_number, return_removed_thing=True)
        self.insert_thing(insertion_position, thing)

    def is_valid_thing_number_str(self, thing_number: str) -> bool:
        return thing_number.isdigit() and 0 <= int(thing_number) - 1 < len(self.things)

    def remove_thing(
        self, thing_number: int, return_removed_thing: bool = False
    ) -> None | Thing:
        if return_removed_thing:
            return self.things.pop(thing_number - 1)
        self.things.pop(thing_number - 1)

    def clear_checklist(self) -> None:
        self.things.clear()

    def check_thing(self, thing: Thing) -> None:
        thing.check()

    def uncheck_thing(self, thing: Thing) -> None:
        thing.uncheck()

    def _all_things_checked(self) -> bool:
        return bool(self.things) and all(thing.checked for thing in self.things)

    def __str__(self) -> str:
        return f"{self.name} ✅" if self._all_things_checked() else f"{self.name}"
