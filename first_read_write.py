#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python
# coding: utf-8

# In[9]:


import threading,random,time,sys
data = 500
total = 0
stop = 0
wthread = []
rthread = []
#sem = threading.Semaphore()
readready = threading.Condition(threading.Lock())
mutexa = threading.Condition(threading.Lock())
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
    while total < 120 and stop == 0:
            #acquire
            mutexa.acquire()
            readcount +=1
            rcount+=1
            if(readcount == 1):
                readready.acquire()
            mutexa.release()

            print("    [Reader%d] enter critical section."%(num))
        
            print("    [Reader%d] read %d"%(num,data))
            times= random.randint(1,4)
            total = total + times
            print("    [Reader%d] sleep %d seconds."%(num,times))
            time.sleep(times)
            print("    [Reader%d] exit critical section."%(num))

            #release
            mutexa.acquire()
            readcount-=1
            if readcount==0:
                readready.release()
            mutexa.release()

            times= random.randint(3,8)
            total = total + times
            #print("[Reader%d] sleep %d seconds."%(num,times))
            time.sleep(times)
    time.sleep(100)
def write(num):
    global data
    global readcount
    global total
    global wcount
    global stop
    while total < 120 and stop == 0:
        #acquire
        readready.acquire()
        
        print("[Writer%d] enter critical section."%(num))
        data = random.randint(0,99)
        print("[Writer%d] write %d"%(num,data))
        times = random.randint(1,4)
        total = total + times
        wcount +=1
        print("[Writer%d] sleep %d seconds."%(num,times))
        time.sleep(times)
        print("[Writer%d] exit critical section."%(num))
        
        #release
        readready.release()

        times= random.randint(1,4)
        total = total + times
        #print("[Reader%d] sleep %d seconds."%(num,times))
        time.sleep(times)
    time.sleep(100)
for i in range(0,Reader):
    rthread.append(threading.Thread(target = read,args = (i,)))
    rthread[i].start()
for j in range(0,Writer,1):
    wthread.append(threading.Thread(target = write,args = (j,)))
    wthread[j].start()

while 1:
   
    if total > 120:
        stop = -1
        time.sleep(20)
        print("\nFirst Reader-Writer stop")
        print("Total write counts:%d"%(wcount))
        print("Total read  counts:%d"%(rcount) )
        sys.exit()




        


# In[ ]:




