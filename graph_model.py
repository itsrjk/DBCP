import numpy as np
import matplotlib.pyplot as plt


x1=["A-TA-NC","A-XR-NC"]
y1=[42.61,38.85]

x2=["A-XR-NC","A-XR-C"]
y2=[38.85,41.16]

x3=["A-XR-NC","M-XR-NC"]
y3=[38.85,40.27]

fig,axs = plt.subplots(1,3)
w=0.1
axs[0].bar(x1,y1,align="center",color="#003f5c",width=0.5)
axs[1].bar(x2,y2,align="center",color="#003f5c",width=0.5)
axs[2].bar(x3,y3,align="center",color="#003f5c",width=0.5)
fig.suptitle("Gross Average Miss Latency")

axs[0].set(ylabel="Avg miss latency in cycles (lesser is better)")

plt.show()

