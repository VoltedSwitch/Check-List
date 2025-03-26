import time
from typing import Any

from colors import cc 
from file_handler import FileHandler
from utilities import clear_screen, show_cursor, hide_cursor


class Thing:
    def __init__(self, sentence: str, is_checked: bool=False) -> None:
        self.sentence: str = sentence
        self.is_checked: bool = is_checked

    def check(self) -> None:
        self.is_checked: bool = True

    def uncheck(self) -> None:
        self.is_checked: bool = False

    def __str__(self) -> str:
        return f"{self.sentence} ✅" if self.is_checked else f"{self.sentence}"


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
    

class ChecklistsManager:
    def __init__(self) -> None:
        self.user_checklists: list[Checklist] = []

    def add_checklist(self, checklist: Checklist) -> None:
        self.user_checklists.append(checklist)

    def insert_checklist(self, checklist: Checklist, checklist_number: int) -> None:
        self.user_checklists.insert(checklist_number - 1, checklist)

    def remove_checklist(self, checklist_number: int) -> None:
        self.user_checklists.pop(checklist_number -  1)

    def clear_all_checklists(self) -> None:
        self.user_checklists.clear()

    def get_checklist(self, checklist_number: int) -> Checklist:
        return self.user_checklists[checklist_number - 1]

    def is_valid_checklist_number_str(self, checklist_number: str) -> bool:
        return checklist_number.isdigit() and (0 <= int(checklist_number) - 1 < len(self.user_checklists))


class UserInterface:
    CREATE_NEW_CHECKLIST = "n"
    INSERT_NEW_CHECKLIST = "k"
    DELETE_CHECKLIST = "d"
    DELETE_ALL_CHECKLISTS = "l"
    SAVE_EXIT = "s"

    ADD_THING = "a"
    INSERT_THING = "i"
    REMOVE_THING = "r"
    CLEAR_CHECKLIST = "c"
    TOGGLE_CHECK = "t"
    EXIT = "e"

    def __init__(self) -> None:
        self.checklists_manager = ChecklistsManager()
        self.load_checklist()
    
    def display_checklist(self, checklist: Checklist) -> None:
        if not checklist.things:
            print(f"Checklist '{checklist}' is currently empty!\n")
            return

        width = len(str(len(checklist.things)))

        print(checklist.name)
        for index, thing in enumerate(checklist.things, start=1):
            print(f"  {index:>{width}}. {thing}")
        print()

    def display_checklist_names(self) -> None:
        if not self.checklists_manager.user_checklists:
            print("You haven't created any checklists yet!\n")
            return
        
        width = len(str(len(self.checklists_manager.user_checklists)))
        
        print("All Your Checklists:")
        for index, checklist in enumerate(self.checklists_manager.user_checklists, start=1):
            print(f"  {index:>{width}}. {checklist}")
        print()

    def main_menu(self) -> str:
        print(f"{self.CREATE_NEW_CHECKLIST}. Create a new checklist")
        print(f"{self.INSERT_NEW_CHECKLIST}. Insert a new checklist")
        print(f"{self.DELETE_CHECKLIST}. Delete an exisiting checklist")
        print(f"{self.DELETE_ALL_CHECKLISTS}. Delete ALL existing checklists")
        print("   -- OR choose a checklist number to open an existing checklist")
        print(f"{self.SAVE_EXIT}. Save/Exit")
        return input("\n> ").strip()
    
    def main_menu_user_interactions_section(self) -> None:
        while True:
            self.display_checklist_names()
            user_input: str = self.main_menu()
            clear_screen()
            if user_input == self.SAVE_EXIT:
                self.save_progress_and_exit()
            elif user_input == self.CREATE_NEW_CHECKLIST:
                self.create_checklist_interface()
            elif user_input == self.INSERT_NEW_CHECKLIST:
                if not self.checklists_manager.user_checklists:
                    print(f"{cc.RED}You have no checklist number position to insert at!{cc.END}\n")
                    continue
                self.insert_checklist_interface()
            elif user_input == self.DELETE_CHECKLIST:
                if not self.checklists_manager.user_checklists:
                    print(f"{cc.RED}You have no checklists to remove!{cc.END}\n")
                    continue
                self.remove_checklist_interface()
            elif user_input == self.DELETE_ALL_CHECKLISTS:
                if not self.checklists_manager.user_checklists:
                    print(f"{cc.RED}You have no checklists to remove!{cc.END}\n")
                    continue
                self.clear_checklists_interface()
            elif self.checklists_manager.is_valid_checklist_number_str(user_input):
                self.checklist_user_interactions_structure(self.checklists_manager.get_checklist(int(user_input)))
            else:
                print(f"{cc.RED}Invalid main menu option!{cc.END}\n")

    def checklist_menu(self) -> str:
        print(f"{self.ADD_THING}. Add thing")
        print(f"{self.INSERT_THING}. Insert thing")
        print(f"{self.REMOVE_THING}. Remove thing")
        print(f"{self.CLEAR_CHECKLIST}. Clear checklist")
        print(f"{self.TOGGLE_CHECK}. Toggle Check")
        print(f"{self.EXIT}. Exit Current Checklist")
        return input("\n> ").strip()
    
    def checklist_user_interactions_structure(self, checklist: Checklist) -> None:
        while True:
            self.display_checklist(checklist)
            user_input: str = self.checklist_menu()
            clear_screen()
            if user_input == self.EXIT:
                return
            elif user_input == self.ADD_THING:
                self.add_thing_interface(checklist)
            elif user_input == self.INSERT_THING:
                if not checklist.things:
                    print(f"{cc.RED}There is no thing number position to insert another thing at!{cc.END}\n")
                    continue
                self.insert_thing_interface(checklist)
            elif user_input == self.REMOVE_THING:
                if not checklist.things:
                    print(f"{cc.RED}You have no things to remove!{cc.END}\n")
                    continue
                self.remove_thing_interface(checklist)
            elif user_input == self.CLEAR_CHECKLIST:
                if not checklist.things:
                    print(f"{cc.RED}You have no things to remove!{cc.END}\n")
                    continue
                self.clear_checklist_interface(checklist)
            elif user_input == self.TOGGLE_CHECK:
                if not checklist.things:
                    print(f"{cc.RED}You have no things to check or uncheck!{cc.END}\n")
                    continue
                self.toggle_check_thing_interface(checklist)
            else:
                print(f"{cc.RED}Invalid menu option!{cc.END}\n")

    def create_checklist_interface(self) -> None:
        while True:
            self.display_checklist_names()
            print("Checklist Creation Mode\n")
            name: str = input("Enter the name of your new checklist (e to exit mode): ").strip()
            clear_screen()
            if name.lower() == "e":
                return
            if name:
                self.checklists_manager.add_checklist(Checklist(name))
                continue
            print(f"{cc.RED}Please enter a valid name!{cc.END}\n")
    
    def insert_checklist_interface(self) -> None:
        while True:
            self.display_checklist_names()
            print("Checklist Insertion Mode\n")
            name: str = input("Enter the name of your new checklist (e to exit mode): ").strip()
            clear_screen()
            if name.lower() == "e":
                return
            if name:
                while True:
                    self.display_checklist_names()
                    print("Checklist Insertion Mode\n")
                    number: str = input("Enter a valid number to insert the checklist at (e to exit mode): ").strip()
                    clear_screen()
                    if number.lower() == "e":
                        return
                    elif self.checklists_manager.is_valid_checklist_number_str(number):
                        self.checklists_manager.insert_checklist(Checklist(name), int(number))
                        break
                    else:
                        print(f"{cc.RED}Please enter a valid number!{cc.END}\n")
            else:
                print(f"{cc.RED}Please enter a valid name!{cc.END}\n")
    
    def remove_checklist_interface(self) -> None:
        while True:
            self.display_checklist_names()
            print("Checklist Deletion Mode\n")
            number: str = input("Enter a valid number of a checklist to remove (e to exit mode): ").strip()
            clear_screen()
            if number.lower() == "e":
                return
            elif self.checklists_manager.is_valid_checklist_number_str(number):
                self.checklists_manager.remove_checklist(int(number))
                continue
            print(f"{cc.RED}Please enter a valid number!{cc.END}\n")
    
    def clear_checklists_interface(self) -> None:
        self.display_checklist_names()
        print("ALL Checklists Clearance Mode\n")
        user_input: str = input("Are you sure you want to delete ALL of your checklists? (y/n): ").strip()
        clear_screen()
        hide_cursor()
        if user_input.lower() == "y":
            self.checklists_manager.clear_all_checklists()
            print("ALL checklists removed successfully")
            time.sleep(2)
            clear_screen()
        else:
            print("ALL of your checklists remained")
            time.sleep(2)
            clear_screen()
        show_cursor()

    def add_thing_interface(self, checklist: Checklist) -> None:
        while True:
            self.display_checklist(checklist)
            print("Add Mode\n")
            thing: str = input("Enter a thing (e to exit mode): ").strip()
            clear_screen()
            if thing.lower() == "e":
                return
            if thing:
                checklist.add_thing(Thing(thing))
                continue
            print(f"{cc.RED}Please Enter a valid thing!{cc.END}\n")

    def insert_thing_interface(self, checklist: Checklist) -> None:
        while True:
            thing_number: int = self.get_valid_thing_number(checklist, "Insert Mode")
            if not thing_number:
                return
            self.display_checklist(checklist)
            print("Insert Mode\n")
            thing: str = input("Enter a thing (e to exit mode): ").strip()
            clear_screen()
            if thing.lower() == "e":
                return
            if thing:
                checklist.insert_thing(Thing(thing), thing_number)
                continue
            print(f"{cc.RED}Please Enter a valid thing!{cc.END}\n")
    
    def get_valid_thing_number(self, checklist: Checklist, mode_to_display: str=None) -> int:
        while True:
            self.display_checklist(checklist)
            if mode_to_display is not None:
                print(mode_to_display + "\n")
            user_input: str = input("Enter a valid number from the checklist (e to exit mode): ").strip()
            clear_screen()
            if user_input.lower() == "e":
                return False
            if checklist.is_valid_thing_number_str(user_input):
                return int(user_input)
            print(f"{cc.RED}Invalid thing number{cc.END}\n")

    def remove_thing_interface(self, checklist: Checklist) -> None:
        while True:
            thing_number: int = self.get_valid_thing_number(checklist, "Removal Mode")
            if not thing_number:
                return
            checklist.remove_thing(thing_number)

    def clear_checklist_interface(self, checklist: Checklist) -> None:
        self.display_checklist(checklist)
        print("Checklist Clearance Mode\n")
        user_input: str = input("Are you sure you want to clear the checklist? (y/n): ")
        clear_screen()
        hide_cursor()
        if user_input.lower() == "y":
            checklist.clear_checklist()
            print("Checklist cleared successfully")
            time.sleep(2)
            clear_screen()
        else:
            print("Checklist was not cleared")
            time.sleep(2)
            clear_screen()
        show_cursor()

    def toggle_check_thing_interface(self, checklist: Checklist) -> None:
        while True:
            thing_number: int = self.get_valid_thing_number(checklist, "Toggle Check Mode")
            if not thing_number:
                return
            thing = checklist.get_thing(thing_number)
            if thing.is_checked:
                checklist.uncheck_thing(thing)
            else:
                checklist.check_thing(thing)

    def save_progress_and_exit(self) -> None:
        data: list[Checklist] = []
        for checklist in self.checklists_manager.user_checklists:
            checklist_data: dict[str, Any] = {
                "name": checklist.name,
                "things": [
                    {"sentence": thing.sentence, "is_checked": thing.is_checked}
                    for thing in checklist.things
                ]
            }
            data.append(checklist_data)
        FileHandler.save_json(data)
        hide_cursor()
        print("Progress saved successfully")
        time.sleep(2)
        clear_screen()
        exit()

    def load_checklist(self) -> None:
        data = FileHandler.load_json()
        for checklist_data in data:
            checklist: Checklist = Checklist(checklist_data["name"])
            for thing_data in checklist_data["things"]:
                thing: Thing = Thing(thing_data["sentence"], thing_data["is_checked"])
                checklist.add_thing(thing)
            self.checklists_manager.add_checklist(checklist)


def main() -> None:
    ui: UserInterface = UserInterface()
    ui.main_menu_user_interactions_section()


if __name__ == "__main__":
    clear_screen()
    main()