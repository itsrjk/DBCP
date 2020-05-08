import numpy as np
import matplotlib.pyplot as plt

N = 10
ind = np.arange(N)  # the x locations for the groups
width = 0.27       # the width of the bars

fig = plt.figure()
ax = fig.add_subplot(111)

# yvals= a-xr-nc
# zvals = m-ta-c
# kvals = no_pref
# k[0],y[0] and x[0] are values of the same trace

###useful pf pc
#ax.set_title("Percentage of useful prefetches")
#ax.set_ylabel('Percentage (more is better)')
#yvals = [33.81,36.72,0]
#zvals = [0.03,0.41,0]
#kvals = [0,0,0]

##IPC
ax.set_ylabel('IPC (more is better)')
ax.set_title("IPC (Instuctions Per Cycle)")
yvals = [0.41,0.68, 1.16,0.687,0.632,1.33,1.06,0.69,0.55,1.25]
zvals = [0.38,0.69,1.14,0.69,0.61,1.30,1.055,0.66,0.52,1.25]
kvals = [0.47,0.72,1.17,0.68,0.69,1.48,1.12,0.95,0.75,1.25]

##L1D avg miss latency
#ax.set_ylabel('Miss latency in cycles(less is better)')
#ax.set_title("Average miss latency")
#yvals = [26.435,50.58,34.09,134.38,23.133,15.73,27.19,14.66,13.67,199.33] 
#zvals = [23.94,66.97,33.63,138.06,22.52,16.77,29.31,15.65,15.02,199.33]
#kvals = [69.91,312,38.10,259.1,39.9,108.4,77.88,90.17,16.16,199.33]

rects1 = ax.bar(ind, yvals, width, color="#003f5c")
rects2 = ax.bar(ind+width, zvals, width, color='#ef5675')
rects3 = ax.bar(ind+width*2, kvals, width, color='#ffa600')

ax.set_xticks(ind+width)
ax.set_xticklabels(('602.gcc_s-734B', '603.bwaves_s-1740B','607.cactuBSSN_s-2421B','619.lbm_s-2676B',
'623.xalancbmk_s-165B','625.x264_s-12B',
'628.pop2_s-17B','631.deepsjeng_s-928B','641.leela_s-149B', '648.exchange2_s-72B'),rotation=90)
ax.legend( (rects1[0], rects2[0], rects3[0]), ('[A-XR-NC]', '[M-TA-C]', 'no_pref'),loc="upper left")

def autolabel(rects):
    for rect in rects:
        h = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1*h, '%.2f'%float(h),
                ha='center', va='bottom')

#autolabel(rects1)
#autolabel(rects2)
#autolabel(rects3)
plt.show()
