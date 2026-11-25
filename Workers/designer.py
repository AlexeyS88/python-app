from Workers.employee import Employee

class Designer(Employee):
    def work(self) -> None:
        print(f"{self._name} рисует интерфейс за {self._salary} руб.")