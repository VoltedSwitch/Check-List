class Thing:
    def __init__(self, sentence: str, is_checked: bool = False) -> None:
        self.sentence: str = sentence
        self.is_checked: bool = is_checked

    def check(self) -> None:
        self.is_checked: bool = True

    def uncheck(self) -> None:
        self.is_checked: bool = False

    def __str__(self) -> str:
        return f"{self.sentence} ✅" if self.is_checked else f"{self.sentence}"
