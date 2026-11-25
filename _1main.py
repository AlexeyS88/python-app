import asyncio

async def fetch_data(seconds:int, id:int) -> bool:
    try:
        print(f"Начинаем запрос c id={id}")
        await asyncio.sleep(seconds)
        print(f"Запрос c id={id} прошел успешно")
        return True
    except Exception as e:
        print(f"Что-то пошло не так: {e}")
        return False 

async def main():
    task1 =  asyncio.create_task(fetch_data(4, 1))
    task2 =  asyncio.create_task(fetch_data(1, 2))
    await asyncio.gather(fetch_data(2, 3), fetch_data(3, 4))
    result1 = await task1
    result2 = await task2
    print(result1, result2)

asyncio.run(main())