class NotEnoughMoneyException(Exception):
    pass


class CurrencyOperations:
    def __init__(self):
        self.count = 0
        try:
            with open("currency.dat", mode="r", encoding="utf-8") as f:
                self.count = int(f.readlines()[0].strip())
        except Exception:
            try:
                with open("currency.dat", mode="w", encoding="utf-8") as f:
                    f.write(str(self.count))
            except Exception:
                print(
                    "Error opening currency.dat"
                )  # Replace with Qt dialog later
                del self

    def write(self) -> None:
        try:
            with open("currency.dat", mode="w", encoding="utf-8") as f:
                f.write(str(self.count))
        except Exception:
            print("Error opening currency.dat")  # Replace with Qt dialog later
            del self

    def add(self, m: int):
        self.count += m
        self.write()

    def buy(self, m: int):
        if self.count - m >= 0:
            self.count -= m
            self.write()
        else:
            raise NotEnoughMoneyException

    def get(self) -> int:
        return self.count
