from checklist_core.user_interface import UserInterface
from utils.utility_funcs import clear_screen

def main() -> None:
    ui: UserInterface = UserInterface()
    ui.main_menu_user_interactions_structure()


if __name__ == "__main__":
    clear_screen()
    main()