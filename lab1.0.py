import asyncio
import websockets

async def start(uri):
    async with websockets.connect(uri) as websocket:
        await websocket.send("Let's start")
        example =  await websocket.recv()
        print(f"{example}")
        mas = example[6:len(example)]
        for i in mas:
            if i == '+':
                a = mas.index(i)
                answer = int(mas[0:(a-1)])+ int(mas[(a+2):len(mas)])
                print('Answer: ',mas,' = ',answer)
            elif i == '-':
                a = mas.index(i)
                answer = int(mas[0:(a-1)])- int(mas[(a+2):len(mas)])
                print('Answer: ',mas,' = ',answer)
            elif i == '*':
                a = mas.index(i)
                answer = int(mas[0:(a-1)])* int(mas[(a+2):len(mas)])
                print('Answer: ',mas,' = ',answer)
        await websocket.send(str(answer))
        print('Done')
asyncio.get_event_loop().run_until_complete(start('wss://sprs.herokuapp.com/zeroth/session-1'))
