import time
from colors import cc 
from file_handler import FileHandler
from utilities import clear_screen, show_cursor, hide_cursor, instant_input


class Thing:
    def __init__(self, sentence: str, is_checked: bool=False) -> None:
        self.sentence: str = sentence
        self.is_checked: bool = is_checked

    def check(self) -> None:
        self.is_checked: bool = True

    def uncheck(self) -> None:
        self.is_checked: bool = False

    def __str__(self) -> str:
        return f"{self.sentence} {'✅' if self.is_checked else ''}"


class Checklist:
    def __init__(self) -> None:
        self.things: list[Thing] = []
    
    def get_thing(self, thing_number: int) -> Thing:
        return self.things[thing_number - 1]
    
    def add_thing(self, thing: Thing) -> None:
        self.things.append(thing)

    def insert_thing(self, thing: Thing, thing_number: int) -> None:
        self.things.insert(thing_number - 1, thing)

    def is_valid_thing_number_str(self, thing_number: str) -> bool:
        if thing_number.isdigit():
            if 0 <= int(thing_number) - 1 < len(self.things):
                return True
        return False

    def remove_thing(self, thing_number: int) -> None:
        self.things.pop(thing_number - 1)

    def clear_checklist(self) -> None:
        self.things.clear()

    def check_thing(self, thing: Thing) -> None:
        thing.check()
    
    def uncheck_thing(self, thing: Thing) -> None:
        thing.uncheck()
    

class UserInterface:
    ADD_THING = "a"
    INSERT_THING = "i"
    REMOVE_THING = "r"
    CLEAR_CHECKLIST = "c"
    TOGGLE_CHECK = "t"
    SAVE_EXIT = "e"

    def __init__(self) -> None:
        self.checklist: Checklist = Checklist()
        self.load_checklist()
    
    def display_checklist(self) -> None:
        if self.checklist.things == []:
            print("Your Checklist is currently empty!\n")
            return
    
        print("Checklist:")
        for index, thing in enumerate(self.checklist.things, start=1):
            print(f"  {index}. {thing}")
        print()
    
    def checklist_interactions_menu(self) -> None:
        print(f"{self.ADD_THING}. Add thing")
        print(f"{self.INSERT_THING}. Insert thing")
        print(f"{self.REMOVE_THING}. Remove thing")
        print(f"{self.CLEAR_CHECKLIST}. Clear checklist")
        print(f"{self.TOGGLE_CHECK}. Toggle Check")
        print(f"{self.SAVE_EXIT}. Save/Exit")
        return instant_input("\n> ")

    def add_thing_interface(self) -> None:
        while True:
            self.display_checklist()
            print("Add Mode\n")
            user_input = input("Enter a thing (e to exit mode): ")
            clear_screen()
            if user_input.lower() == "e":
                return
            if user_input != "":
                thing = Thing(user_input)
                self.checklist.add_thing(thing)
                continue
            print(f"{cc.RED}Please Enter a valid thing!{cc.END}\n")

    def insert_thing_interface(self) -> None:
        while True:
            thing_number = self.get_valid_thing_number("Insert Mode")
            if not thing_number:
                return
            self.display_checklist()
            print("Insert Mode\n")
            user_input = input("Enter a thing (e to exit mode): ")
            clear_screen()
            if user_input.lower() == "e":
                return
            if user_input != "":
                thing = Thing(user_input)
                self.checklist.insert_thing(thing, thing_number)
                continue
            print(f"{cc.RED}Please Enter a valid thing!{cc.END}\n")
    
    def get_valid_thing_number(self, mode_to_display: str=None) -> int:
        while True:
            self.display_checklist()
            if mode_to_display is not None:
                print(mode_to_display + "\n")
            user_input: str = input("Enter a valid number from the checklist (e to exit mode): ").strip()
            clear_screen()
            if user_input.lower() == "e":
                return False
            if self.checklist.is_valid_thing_number_str(user_input):
                return int(user_input)
            print(f"{cc.RED}Invalid thing number{cc.END}\n")

    def remove_thing_interface(self) -> None:
        while True:
            thing_number = self.get_valid_thing_number("Removal Mode")
            if not thing_number:
                return
            self.checklist.remove_thing(thing_number)

    def clear_checklist_interface(self) -> None:
        self.display_checklist()
        user_input = input("Are you sure you want to clear the checklist? (y/n): ")
        clear_screen()
        hide_cursor()
        if user_input.lower() == "y":
            self.checklist.clear_checklist()
            print("Checklist cleared successfully")
            time.sleep(2)
            clear_screen()
        else:
            print("Checklist was not cleared")
            time.sleep(2)
            clear_screen()
        show_cursor()

    def toggle_check_thing_interface(self):
        while True:
            thing_number = self.get_valid_thing_number("Toggle Check Mode")
            if not thing_number:
                return
            thing = self.checklist.get_thing(thing_number)
            if thing.is_checked:
                self.checklist.uncheck_thing(thing)
            else:
                self.checklist.check_thing(thing)

    def save_checklist_and_exit(self) -> None:
        data: list = [
            {"sentence": thing.sentence, "is_checked": thing.is_checked}
            for thing in self.checklist.things
        ]
        FileHandler.save_json(data)
        hide_cursor()
        print("Checklist saved successfully")
        time.sleep(2)
        clear_screen()
        exit()

    def load_checklist(self) -> None:
        data = FileHandler.load_json()
        for thing_data in data:
            thing = Thing(thing_data["sentence"], thing_data["is_checked"])
            self.checklist.add_thing(thing)


def main() -> None:
    ui: UserInterface = UserInterface()
    while True:
        ui.display_checklist()
        user_input = ui.checklist_interactions_menu()
        clear_screen()
        if user_input == ui.ADD_THING:
            ui.add_thing_interface()
        elif user_input == ui.INSERT_THING:
            ui.insert_thing_interface()
        elif user_input == ui.REMOVE_THING:
            if ui.checklist.things == []:
                print(f"{cc.RED}You have nothing to remove!{cc.END}\n")
                continue
            ui.remove_thing_interface()
        elif user_input == ui.CLEAR_CHECKLIST:
            if ui.checklist.things == []:
                print(f"{cc.RED}You have nothing to clear!{cc.END}\n")
                continue
            ui.clear_checklist_interface()
        elif user_input == ui.TOGGLE_CHECK:
            if ui.checklist.things == []:
                print(f"{cc.RED}You have nothing to check or uncheck!{cc.END}\n")
                continue
            ui.toggle_check_thing_interface()
        elif user_input == ui.SAVE_EXIT:
            ui.save_checklist_and_exit()
        else:
            print(f"{cc.RED}Invalid menu option!{cc.END}\n")


if __name__ == "__main__":
    clear_screen()
    main()