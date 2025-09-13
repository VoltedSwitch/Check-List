import time
from typing import Any

from .checklist_manager import ChecklistsManager
from .checklist import Checklist
from .item import Item
from utils.file_handler import FileHandler
from utils.utility_funcs import clear_screen, hide_cursor, show_cursor
from utils.colors import c


class UserInterface:
    CREATE_NEW_CHECKLIST = "n"
    INSERT_NEW_CHECKLIST = "k"
    RENAME_CHECKLIST = "h"
    REPOSITION_CHECKLIST = "w"
    DELETE_CHECKLIST = "d"
    DELETE_ALL_CHECKLISTS = "l"
    SAVE_EXIT = "s"

    ADD_ITEM = "a"
    INSERT_ITEM = "i"
    RENAME_ITEM = "m"
    REPOSITION_ITEM = "g"
    REMOVE_ITEM = "r"
    CLEAR_CHECKLIST = "c"
    TOGGLE_CHECK = "t"
    EXIT = "e"

    def __init__(self) -> None:
        self.checklists_manager: ChecklistsManager = ChecklistsManager()
        self.load_checklist()

    def main_menu(self) -> str:
        print(f"{self.CREATE_NEW_CHECKLIST}. Create new checklist")
        print(f"{self.INSERT_NEW_CHECKLIST}. Insert new checklist")
        print(f"{self.RENAME_CHECKLIST}. Rename checklist")
        print(f"{self.REPOSITION_CHECKLIST}. Reposition checklist")
        print(f"{self.DELETE_CHECKLIST}. Delete an exisiting checklist")
        print(f"{self.DELETE_ALL_CHECKLISTS}. Delete ALL existing checklists")
        print("#. OR choose a checklist number to open an existing checklist")
        print(f"{self.SAVE_EXIT}. Save/Exit")
        return input("\n> ").strip()

    def main_menu_user_interactions_structure(self) -> None:
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
                    print(
                        f"{c.RED}You have no checklist number position to insert at!{c.END}\n"
                    )
                    continue
                self.insert_checklist_interface()
            elif user_input == self.RENAME_CHECKLIST:
                if not self.checklists_manager.user_checklists:
                    print(f"{c.RED}You have no checklist to rename!{c.END}\n")
                    continue
                self.rename_checklist_interface()
            elif user_input == self.REPOSITION_CHECKLIST:
                if not self.checklists_manager.user_checklists:
                    print(f"{c.RED}You have no checklists to reposition!{c.END}\n")
                    continue
                self.reposition_checklist_interface()
            elif user_input == self.DELETE_CHECKLIST:
                if not self.checklists_manager.user_checklists:
                    print(f"{c.RED}You have no checklists to remove!{c.END}\n")
                    continue
                self.remove_checklist_interface()
            elif user_input == self.DELETE_ALL_CHECKLISTS:
                if not self.checklists_manager.user_checklists:
                    print(f"{c.RED}You have no checklists to remove!{c.END}\n")
                    continue
                self.clear_checklists_interface()
            elif self.checklists_manager.is_valid_checklist_number_str(user_input):
                self.checklist_user_interactions_structure(
                    self.checklists_manager.get_checklist(int(user_input))
                )
            else:
                print(f"{c.RED}Invalid main menu option!{c.END}\n")

    def checklist_menu(self) -> str:
        print(f"{self.ADD_ITEM}. Add item")
        print(f"{self.INSERT_ITEM}. Insert item")
        print(f"{self.RENAME_ITEM}. Rename item")
        print(f"{self.REPOSITION_ITEM}. Reposition item")
        print(f"{self.REMOVE_ITEM}. Remove item")
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
            elif user_input == self.ADD_ITEM:
                self.add_item_interface(checklist)
            elif user_input == self.INSERT_ITEM:
                if not checklist.items:
                    print(
                        f"{c.RED}There is no item number position to insert another item at!{c.END}\n"
                    )
                    continue
                self.insert_item_interface(checklist)
            elif user_input == self.RENAME_ITEM:
                if not checklist.items:
                    print(f"{c.RED}There is no item to rename!{c.END}\n")
                    continue
                self.rename_item_interface(checklist)
            elif user_input == self.REPOSITION_ITEM:
                if not checklist.items:
                    print(f"{c.RED}There is no item to reposition!{c.END}\n")
                    continue
                self.reposition_item_interface(checklist)
            elif user_input == self.REMOVE_ITEM:
                if not checklist.items:
                    print(f"{c.RED}You have no items to remove!{c.END}\n")
                    continue
                self.remove_item_interface(checklist)
            elif user_input == self.CLEAR_CHECKLIST:
                if not checklist.items:
                    print(f"{c.RED}You have no items to remove!{c.END}\n")
                    continue
                self.clear_checklist_interface(checklist)
            elif user_input == self.TOGGLE_CHECK:
                if not checklist.items:
                    print(f"{c.RED}You have no items to check or uncheck!{c.END}\n")
                    continue
                self.toggle_check_item_interface(checklist)
            else:
                print(f"{c.RED}Invalid menu option!{c.END}\n")

    def display_checklist(self, checklist: Checklist) -> None:
        if not checklist.items:
            print(f"Checklist '{checklist.name}' is currently empty!\n")
            return

        width = len(str(len(checklist.items)))

        print(checklist.name)
        for index, item in enumerate(checklist.items, start=1):
            print(f"  {index:>{width}}. {item}")
        print()

    def display_checklist_names(self) -> None:
        if not self.checklists_manager.user_checklists:
            print("You haven't created any checklists yet!\n")
            return

        width = len(str(len(self.checklists_manager.user_checklists)))

        print("All Your Checklists:")
        for index, checklist in enumerate(
            self.checklists_manager.user_checklists, start=1
        ):
            print(f"  {index:>{width}}. {checklist}")
        print()

    def create_checklist_interface(self) -> None:
        while True:
            self.display_checklist_names()
            print("Checklist Creation Mode\n")
            name: str = input("Enter the name of your new checklist (e to exit mode): ")
            clear_screen()
            if name.lower() == "e":
                return
            elif name:
                self.checklists_manager.add_checklist(Checklist(name))
                continue
            print(f"{c.RED}Please enter a valid name!{c.END}\n")

    def add_item_interface(self, checklist: Checklist) -> None:
        while True:
            self.display_checklist(checklist)
            print("item Add Mode\n")
            item: str = input("Enter a item (e to exit mode): ")
            clear_screen()
            if item.lower() == "e":
                return
            elif item:
                checklist.add_item(Item(item))
                continue
            print(f"{c.RED}Please enter a valid item!{c.END}\n")

    def insert_checklist_interface(self) -> None:
        while True:
            checklist_number: int | None = self.get_valid_checklist_number(
                "Checklist Insertion Mode"
            )
            if not checklist_number:
                return
            while True:
                self.display_checklist_names()
                print("Checklist Insertion Mode\n")
                name: str = input(
                    f"Enter the name of your new checklist to insert at #{checklist_number} (e to exit mode): "
                )
                clear_screen()
                if name.lower() == "e":
                    return
                elif name:
                    self.checklists_manager.insert_checklist(
                        checklist_number, Checklist(name)
                    )
                    break
                print(f"{c.RED}Please enter a valid name!{c.END}\n")

    def insert_item_interface(self, checklist: Checklist) -> None:
        while True:
            item_number: int | None = self.get_valid_item_number(
                checklist, "item Insert Mode"
            )
            if not item_number:
                return
            while True:
                self.display_checklist(checklist)
                print("item Insert Mode\n")
                item: str = input(
                    f"Enter a item to insert at #{item_number} (e to exit mode): "
                )
                clear_screen()
                if item.lower() == "e":
                    return
                elif item:
                    checklist.insert_item(item_number, Item(item))
                    break
                print(f"{c.RED}Please enter a valid item!{c.END}\n")

    def rename_checklist_interface(self) -> None:
        while True:
            checklist_number: int | None = self.get_valid_checklist_number(
                "Checklist Renaming Mode"
            )
            if not checklist_number:
                return
            while True:
                self.display_checklist_names()
                print("Checklist Renaming Mode\n")
                new_name: str = input(
                    f"Enter a new name for checklist #{checklist_number} (e to exit mode): "
                )
                clear_screen()
                if new_name.lower() == "e":
                    return
                elif new_name:
                    self.checklists_manager.rename_checklist(checklist_number, new_name)
                    break
                print(f"{c.RED}Please enter a valid name!{c.END}\n")

    def rename_item_interface(self, checklist: Checklist) -> None:
        while True:
            item_number: int | None = self.get_valid_item_number(
                checklist, "item Renaming Mode"
            )
            if not item_number:
                return
            while True:
                self.display_checklist(checklist)
                print("item Renaming Mode\n")
                new_name: str = input(
                    f"Enter a new name for item #{item_number} (e to exit mode): "
                )
                clear_screen()
                if new_name.lower() == "e":
                    return
                elif new_name:
                    checklist.rename_item(item_number, new_name)
                    break
                print(f"{c.RED}Please enter a valid name!{c.END}\n")

    def reposition_checklist_interface(self):
        while True:
            checklist_number: int | None = self.get_valid_checklist_number(
                "Checklist Repositioning Mode"
            )
            if not checklist_number:
                return
            while True:
                new_position_number: int | None = self.get_valid_checklist_number(
                    "Checklist Repositioning Mode",
                    f"Enter a valid checklist number to reposition checklist #{checklist_number} to (e to exit mode): ",
                )
                if not new_position_number:
                    return
                elif new_position_number:
                    self.checklists_manager.reposition_checklist(
                        checklist_number, new_position_number
                    )
                    break

    def reposition_item_interface(self, checklist: Checklist):
        while True:
            item_number: int | None = self.get_valid_item_number(
                checklist, "item Repositioning Mode"
            )
            if not item_number:
                return
            while True:
                new_position_number: int | None = self.get_valid_item_number(
                    checklist,
                    "item Repositioning Mode",
                    f"Enter a valid item number to reposition item #{item_number} to (e to exit mode): ",
                )
                if not new_position_number:
                    return
                elif new_position_number:
                    checklist.reposition_item(item_number, new_position_number)
                    break

    def remove_checklist_interface(self) -> None:
        while True:
            checklist_number: int | None = self.get_valid_checklist_number(
                "Checklist Deletion Mode"
            )
            if not checklist_number:
                return
            self.checklists_manager.remove_checklist(checklist_number)

    def remove_item_interface(self, checklist: Checklist) -> None:
        while True:
            item_number: int | None = self.get_valid_item_number(
                checklist, "item Removal Mode"
            )
            if not item_number:
                return
            checklist.remove_item(item_number)

    def clear_checklists_interface(self) -> None:
        self.display_checklist_names()
        print("ALL Checklists Clearance Mode\n")
        user_input: str = input(
            "Are you sure you want to delete ALL of your checklists? (y/n): "
        ).strip()
        clear_screen()
        hide_cursor()
        if user_input.lower() == "y":
            self.checklists_manager.clear_all_checklists()
            print("ALL checklists REMOVED successfully")
            time.sleep(2)
            clear_screen()
        else:
            print("ALL of your checklists REMAINED")
            time.sleep(2)
            clear_screen()
        show_cursor()

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

    def toggle_check_item_interface(self, checklist: Checklist) -> None:
        while True:
            item_number: int | None = self.get_valid_item_number(
                checklist, "Toggle Check Mode"
            )
            if not item_number:
                return
            item = checklist.get_item(item_number)
            if item.checked:
                checklist.uncheck_item(item)
            else:
                checklist.check_item(item)

    def get_valid_checklist_number(
        self, mode_to_display: str | None = None, custom_sentence: str | None = None
    ) -> int | None:
        while True:
            self.display_checklist_names()
            if mode_to_display:
                print(mode_to_display + "\n")
            user_input: str = input(
                "Enter a valid checklist number (e to exit mode): "
                if custom_sentence is None
                else custom_sentence
            ).strip()
            clear_screen()
            if user_input.lower() == "e":
                return None
            elif self.checklists_manager.is_valid_checklist_number_str(user_input):
                return int(user_input)
            print(f"{c.RED}Invalid checklist number{c.END}\n")

    def get_valid_item_number(
        self,
        checklist: Checklist,
        mode_to_display: str | None = None,
        custom_sentence: str | None = None,
    ) -> int | None:
        while True:
            self.display_checklist(checklist)
            if mode_to_display:
                print(mode_to_display + "\n")
            user_input: str = input(
                "Enter a valid number from the checklist (e to exit mode): "
                if custom_sentence is None
                else custom_sentence
            ).strip()
            clear_screen()
            if user_input.lower() == "e":
                return None
            elif checklist.is_valid_item_number_str(user_input):
                return int(user_input)
            print(f"{c.RED}Invalid item number{c.END}\n")

    def save_progress_and_exit(self) -> None:
        data: list[dict[str, Any]] = []
        for checklist in self.checklists_manager.user_checklists:
            checklist_data: dict[str, Any] = {
                "name": checklist.name,
                "items": [
                    {"sentence": item.text, "is_checked": item.checked}
                    for item in checklist.items
                ],
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
            for item_data in checklist_data["items"]:
                item: Item = Item(item_data["sentence"], item_data["is_checked"])
                checklist.add_item(item)
            self.checklists_manager.add_checklist(checklist)
