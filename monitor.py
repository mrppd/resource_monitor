# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 16:36:20 2020

@author: Pronaya
"""

import psutil
import threading
import matplotlib.pyplot as plt
import numpy as np


process_name = "msedge.exe"
#process_name = "chrome.exe"
times = 20

memUseList = []
cpuUseList = []


sumCPU_lock = threading.Lock()
#sumMem_lock = threading.Lock()
sumCPU = 0.0
sumMem = 0.0

def sumProcessInfo(p):   
    global sumCPU, sumMem
    with sumCPU_lock:
        sumCPU += p.cpu_percent(interval=1.0)
        sumMem += p.memory_info().rss/(1024*1024)

def measureUsages():
    global sumCPU, sumMem
    sumCPU = 0.0
    sumMem = 0.0
    thread_list = []
    for proc in psutil.process_iter():
        if proc.name() == process_name :
            try:
                pinfo = proc.as_dict(attrs=['pid'])
            except psutil.NoSuchProcess:
                pass
            else:
                p = psutil.Process(int(pinfo['pid']))
                th = threading.Thread(target=sumProcessInfo, args=(p,))
                thread_list.append(th)
                th.start()
                
                #print(p.cpu_percent())
    
    [t.join() for t in thread_list]
    
    cpuUseList.append(sumCPU/psutil.cpu_count())
    memUseList.append(sumMem)
    print(sumCPU/psutil.cpu_count())
    print(sumMem)
   
for i in range(times):
    print(i)
    measureUsages()
    
#cpuUseList_chrome = cpuUseList[0:20]
#memUseList_chrome = memUseList[0:20]

#cpuUseList_edge = cpuUseList[0:20]
#memUseList_edge = memUseList[0:20]

path = "G:/Work/Programming work/ChromeVSEdge/"
    
plt.plot(range(len(cpuUseList_chrome)), cpuUseList_chrome, 
         label="Chrome. Avg use = "+ str(round(np.mean(cpuUseList_chrome), 2))+"%")
plt.plot(range(len(cpuUseList_edge)), cpuUseList_edge, 
         label="Edge. Avg use = "+str(round(np.mean(cpuUseList_edge), 2))+"%")
plt.title("CPU use Chrome vs Edge (lower is better)")
plt.ylabel('CPU use (%)')
plt.xlabel('Interval ')
plt.legend(loc="upper Right")
plt.savefig(path+'CPUu.png', bbox_inches='tight', dpi=300)
    


plt.plot(range(len(memUseList_chrome)), memUseList_chrome, 
         label="Chrome. Avg use = "+ str(round(np.mean(memUseList_chrome), 2))+"MB")
plt.plot(range(len(memUseList_edge)), memUseList_edge, 
         label="Edge. Avg use = "+str(round(np.mean(memUseList_edge), 2))+"MB")
plt.title("Memory use Chrome vs Edge (lower is better)")
plt.ylabel('Memory use (MB)')
plt.xlabel('Interval ')
plt.legend(loc="upper right")
plt.savefig(path+'Memu.png', bbox_inches='tight', dpi=300)
    
