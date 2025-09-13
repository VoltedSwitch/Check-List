class Thing:
    def __init__(self, text: str, checked: bool = False) -> None:
        self.text: str = text
        self.checked: bool = checked

    def check(self) -> None:
        self.checked: bool = True

    def uncheck(self) -> None:
        self.checked: bool = False

    def __str__(self) -> str:
        return f"{self.text} ✅" if self.checked else self.text
