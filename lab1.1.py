import asyncio
import websockets

async def start(uri):
    async with websockets.connect(uri) as websocket:
        width = 2
        height = 2
        noise = 0.1
        steps = 10
        shuffle = False
        await websocket.send("Let's start")
        number = await websocket.recv()
        numbers = number.split()
        setting = str(width)+" "+str(height)+" "+str(noise)+" "+str(steps)
        if shuffle == True:
            setting = setting+" on"
        else:
            setting = setting+" off"
        await websocket.send(setting)
        width = width * int(numbers[0])
        height = height * int(numbers[1])
        N = int(numbers[2])
        print(str(width))
        matrix = await websocket.recv()
        matrixs = matrix.split()
        print(matrix)
        print("-------")
        for i in range(steps):
            await websocket.send("Ready")
            newmatrix = await websocket.recv()
            newmatrixs = newmatrix.split()
            print(newmatrix)
            length = height*width
            minones = length + 1
            curones = 0
            minindex = 0
            for j in range(N):
                start = 1+ j*(length+1)
                for k in range(length):
                    curones += int(bool(int(newmatrixs[k+1]))^bool(int(matrixs[start+k])))
                if curones<minones:
                    minones = curones
                    minindex = j
                curones = 0
            answer = newmatrixs[0]+" "+matrixs[minindex*(1+length)]
            print(answer)
            print("-------")
            await websocket.send(answer)
            true = await websocket.recv()
            print(true)
            print("-------")
        await websocket.send("Bye")
        rigthanswers = await websocket.recv()
        print(rigthanswers)
asyncio.get_event_loop().run_until_complete(start('wss://sprs.herokuapp.com/first/session-1'))
