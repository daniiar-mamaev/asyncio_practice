import asyncio
import time


# имитация  асинхронного соединения с некой периферией
async def get_conn(host, port):
    class Conn:
        async def put_data(self):
            print('Отправка данных...')
            await asyncio.sleep(2)
            print('Данные отправлены')

        async def get_data(self):
            print('Получение данных...')
            await asyncio.sleep(2)
            print('Данные получены')

        async def close(self):
            print('Завершение соединения...')
            await asyncio.sleep(2)
            print('Соединение завершено')

    print('Устанавливаем соединение...')
    await asyncio.sleep(2)
    print('Соединение установлено')
    return Conn()


class Connection:
    # этот конструктор будет выполнен в заголовке with
    def __init__(self, host, port):
        self.host = host
        self.port = port

    # этот метод будет неявно выполнен при входе в with
    async def __aenter__(self):
        self.conn = await get_conn(self.host, self.port)
        return self.conn

    # этот метод будет неявно выполнен при выходе из with
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.conn.close()


async def main():
    async with Connection('localhost', 9001) as conn:
        send_task = asyncio.create_task(conn.put_data())
        receive_task = asyncio.create_task(conn.get_data())

        # операции отправки и получения данных выполняем конкурентно
        await send_task
        await receive_task


asyncio.run(main())


# async def fun1(x):
#     print(x**2)
#     await asyncio.sleep(3)
#     print('fun1 complete')
#
#
# async def fun2(x):
#     print(x**0.5)
#     await asyncio.sleep(3)
#     print('fun2 complete')
#
#
# async def main():
#     task1 = asyncio.create_task(fun1(4))
#     task2 = asyncio.create_task(fun2(4))
#
#     print(type(task1))
#     print(task1.__class__.__bases__)
#
#     await task1
#     await task2
#
#
# print(time.strftime('%X'))
#
# asyncio.run(main())
#
# print(time.strftime('%X'))
