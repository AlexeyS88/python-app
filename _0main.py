from Workers.tester import Tester
from Workers.developer import Developer
from Workers.designer import Designer

import math
from typing import IO
import time

tester = Tester(name="Irina", salary=1000)
print(tester.__dict__)
tester.work()

developer = Developer(name="Marina", salary=1200, language="python")
developer.work()

designer = Designer(name="Kristina", salary=800)
designer.work()

# with open('./data.txt', 'a+') as data:
#     data.write("\nNew line")
#     data.seek(0)
#     print(data.read())

class FileOpener:
    def __init__(self, file_path:str, mode:str) -> None:
            self.file_path = file_path
            self.mode = mode

    def __enter__(self) -> IO:
        self.file = open(self.file_path, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_value, exc_tb) -> bool:
        self.file.close()
        print(f"Ошибка внутри: {exc_type}, текст {exc_value}")
        return True

with FileOpener('./data.txt', 'r') as data:
    print(data.read())
    raise ValueError("Error: i don't know")
def decorator_timer(func):
    def wrapper():
        start:float = time.time()
        print(f"Начало исполнения: {start:.3f}")
        func()
        end:float = time.time()
        res:float = end - start
        print(f"Конец исполнения {round(res)}")
    return wrapper

@decorator_timer
def load_file() -> None:
    print("Загрузка видео")
    time.sleep(2)

load_file()
     