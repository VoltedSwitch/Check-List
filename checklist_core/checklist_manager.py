from .checklist import Checklist

class ChecklistsManager:
    def __init__(self) -> None:
        self.user_checklists: list[Checklist] = []

    def add_checklist(self, checklist: Checklist) -> None:
        self.user_checklists.append(checklist)

    def insert_checklist(self, checklist_number: int, checklist: Checklist,) -> None:
        self.user_checklists.insert(checklist_number - 1, checklist)

    def rename_checklist(self, checklist_number: int, checklist_new_name: str) -> None:
        self.get_checklist(checklist_number).name = checklist_new_name

    def reposition_checklist(self, checklist_number: int, insertion_position: int) -> None:
        checklist: Checklist = self.remove_checklist(checklist_number, return_removed_checklist=True)
        self.insert_checklist(insertion_position, checklist)

    def remove_checklist(self, checklist_number: int, return_removed_checklist: bool=False) -> None | Checklist:
        if return_removed_checklist:
            return self.user_checklists.pop(checklist_number -  1)
        self.user_checklists.pop(checklist_number -  1)
        
    def clear_all_checklists(self) -> None:
        self.user_checklists.clear()

    def get_checklist(self, checklist_number: int) -> Checklist:
        return self.user_checklists[checklist_number - 1]

    def is_valid_checklist_number_str(self, checklist_number: str) -> bool:
        return checklist_number.isdigit() and (0 <= int(checklist_number) - 1 < len(self.user_checklists))