import launchpad_py as launchpad
import time, random, threading

  
lp = launchpad.LaunchpadPro()

lp.Open()

sw = True
end = False
grid = []
inputP = 0
cc = 36

def input_thread():
    global inputP
    global end
    while not end:
        tmp = lp.EventRaw()
        if tmp != [] and tmp[0][0][1] > 10 and tmp[0][0][1] < 89 and str(tmp[0][0][1])[1] != '0' and str(tmp[0][0][1])[1] != '9':
            inputP = tmp[0][0][1]
        
def collision_thread():
    global end
    global grid
    buffer = True
    tmp = 0
    while not end:
        if buffer:
            tmp = inputP
            buffer = False
        if tmp != inputP:
            tmp = inputP
            if(inputP not in grid):
                end = True
        if grid != []:
            if inputP == grid[0]:
                del(grid[0])
        time.sleep(0.05)
    
            

def death():
    lp.LedAllOn(5)
    time.sleep(0.3)
    lp.Reset()
    time.sleep(0.3)
    lp.LedAllOn(5)
    time.sleep(0.3)
    lp.Reset()
    time.sleep(0.3)
    lp.LedAllOn(5)
    time.sleep(0.3)
    lp.Reset()
    time.sleep(0.3)


x = threading.Thread(target=input_thread)
x.start()

y = threading.Thread(target=collision_thread)
y.start()
while not end:
    time.sleep(0.5)
    lp.Reset()

    #spawn new note
    note = random.randint(91,98)
    grid.append(note)
    
    tmp = lp.EventRaw()
    for i in range(0,len(grid)):
        grid[i] -= 10

    #render notes
    for j,i in enumerate(grid,0):
        if(i < 10):
            lp.Reset()
            end = True
            death()
            break
        else:
            lp.LedCtrlRawByCode(i, cc )

death()

lp.Close()