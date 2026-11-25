from Workers.employee import Employee

class Developer(Employee):
    def __init__(self, name:str, salary:int, language:str):
        super().__init__(name, salary)
        self.language = language

    def work(self) -> None:
        print(f"{self._name} разрабатывает код на языке {self.language}")