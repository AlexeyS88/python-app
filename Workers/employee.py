class Employee:
    def __init__(self, name:str, salary:int):
        self._name = name
        self._salary = salary

    def work(self) -> None:
        print(f"{self._name} работает за {self._salary} руб.")