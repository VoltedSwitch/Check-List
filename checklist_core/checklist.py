from .item import Item


class Checklist:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.items: list[Item] = []

    def get_item(self, item_number: int) -> Item:
        return self.items[item_number - 1]

    def add_item(self, item: Item) -> None:
        self.items.append(item)

    def insert_item(self, item_number: int, item: Item) -> None:
        self.items.insert(item_number - 1, item)

    def rename_item(self, item_number: int, new_text: str) -> None:
        self.get_item(item_number).text = new_text

    def reposition_item(self, item_number: int, insertion_position: int) -> None:
        item: Item = self.remove_item(item_number, return_removed_item=True)
        self.insert_item(insertion_position, item)

    def is_valid_item_number_str(self, item_number: str) -> bool:
        return item_number.isdigit() and 0 <= int(item_number) - 1 < len(self.items)

    def remove_item(
        self, item_number: int, return_removed_item: bool = False
    ) -> None | Item:
        if return_removed_item:
            return self.items.pop(item_number - 1)
        self.items.pop(item_number - 1)

    def clear_checklist(self) -> None:
        self.items.clear()

    def check_item(self, item: Item) -> None:
        item.check()

    def uncheck_item(self, item: Item) -> None:
        item.uncheck()

    def _all_items_checked(self) -> bool:
        return bool(self.items) and all(item.checked for item in self.items)

    def __str__(self) -> str:
        return f"{self.name} ✅" if self._all_items_checked() else f"{self.name}"
