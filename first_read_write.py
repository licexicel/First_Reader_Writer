# First_Reader_Writer
# can multi read but one write at the same time 

import threading,random,time,sys
data = 500
total = 0
stop = 0
wthread = []
rthread = []
sem = threading.Semaphore()
readready = threading.Condition(threading.Lock())
readcount = 0
rcount = 0
wcount = 0
Reader = int(input("How many Readers? "))
Writer = int(input("How many Writers? "))

def read(num):
    global data
    global readcount
    global total
    global rcount
    global stop
    while total < 20 and stop == 0:
            #acquire
            readready.acquire()
            try:
                readcount +=1
                print("[Reader%d] enter critical section."%(num))
                print("[Reader%d] read %d"%(num,data))
                times= random.randint(1,4)
                total = total + times
                print("[Reader%d] sleep %d seconds."%(num,times))
                time.sleep(times)
            finally:
                readready.release()
                rcount +=1
            #release
            readready.acquire()
            try:
                readcount-=1
                if not readcount:
                    readready.notifyAll()
            finally:
                readready.release()
                print("[Reader%d] exit critical section."%(num))
    
    time.sleep(100)
def write(num):
    global data
    global readcount
    global total
    global wcount
    global stop
    while total < 20 and stop == 0:
        #acquire
        readready.acquire()
        while readcount > 0:
            readready.wait()
        print("[Writer%d] enter critical section."%(num))
        data = random.randint(0,99)
        print("[Writer%d] write %d"%(num,data))
        times = random.randint(1,4)
        total = total + times
        wcount +=1
        print("[Writer%d] sleep %d seconds."%(num,times))
        time.sleep(times)
        #release
        readready.release()
        print("[Writer%d] exit critical section."%(num))

    time.sleep(100)
for i in range(0,Reader):
    rthread.append(threading.Thread(target = read,args = (i,)))
    rthread[i].start()
for j in range(0,Writer,1):
    wthread.append(threading.Thread(target = write,args = (j,)))
    wthread[j].start()

while 1:
   
    if total > 20:
        stop = -1
        time.sleep(20)
        print("\nFirst Reader-Writer stop")
        print("Total write counts:%d"%(wcount))
        print("Total read  counts:%d"%(rcount) )
        sys.exit()




        


# In[ ]:




