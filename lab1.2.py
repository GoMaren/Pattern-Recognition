import asyncio
import websockets
async def start(uri):
    async with websockets.connect(uri) as websocket:
        width = 10
        # It can be "L1" or number
        loss = "L1"
        step = 1
        repeat = 3
        await websocket.send("Let's start with "+str(width)+" "+str(loss)+" "+str(step)+" "+str(repeat))
        areyouready = await websocket.recv()
        for i in range(step):
            await websocket.send("Ready")
            heatmap = await websocket.recv()
            heatmaps = heatmap.split()
            print(heatmap)
            print("-------")
            if ( loss == "L1" ):
                summ = 0
                for j in range(width):
                    summ += int(heatmaps[j + 2])
                k = 0
                newsumm = 0.0
                while (newsumm<(float(summ)/2.)):   
                    newsumm = newsumm + float(heatmaps[k + 2])
                    k += 1
                k -= 1
                answer = heatmaps[1]+"\n"+str(k)
                for j in range(1, repeat):
                    answer += " "+str(k)
                print(answer)
                await websocket.send(answer)
                print("-------")
                rightanswer = await websocket.recv()
                print( rightanswer)
                print("-------")
            else:
                #we will use it later
                heatmaps.append("0")
                sums = []
                for j in range(width):
                    sums.append(0)
                for j in range(loss+1):
                    sums[0] += int(heatmaps[j+2])
                for j in range(1, loss+1):
                    sums[j] = sums[j-1]+int(heatmaps[min(j+loss, width)+2])
                #here we are decreasing by the left value of previous sum
                #and increasing by the next after the rigth value of the previos sum
                #but it might happen, that we will go to close to the end of
                #heatmap and that is why we are using the "0" in the end of heatmap
                for j in range(loss+1, width):
                    sums[j] = sums[j-1]-int(heatmaps[j-loss+1])+int(heatmaps[min(j+loss, width)+2])
                print(sums)
                print("-------")
                maxheatmap = 0
                k = 0
                for j in range(width):
                    if sums[j] > maxheatmap:
                        maxheatmap = sums[j]
                        k = j
                answer = heatmaps[1]+"\n"+str(k)
                for j in range(1, repeat):
                    answer += " "+str(k)
                print(answer)
                print("-------")
                await websocket.send(answer)
                rightanswer = await websocket.recv()
                print( rightanswer)
                print("-------")
        await websocket.send("Bye")
        rigthanswers = await websocket.recv()
        print(rigthanswers)
asyncio.get_event_loop().run_until_complete(start('wss://sprs.herokuapp.com/second/session-1'))


