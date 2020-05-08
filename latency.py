import os
import re
import math

folder="./[XR-NC]/[M-XR-NC]/"
line_no=0

if (folder=="no_pref/"):
    line_no=40
elif (folder.startswith("./[TA-C]/")):
    line_no=44
elif (folder.startswith("./[TA-NC]/")):
    line_no=42
elif (folder.startswith("./[XR-NC]/")):
    line_no=42
elif (folder.startswith("./[XR-C]/")):
    line_no=44

os.chdir(folder)
traces=os.listdir(os.getcwd())
#print(traces)

avg_miss_latency=0
no_of_traces=34


for trace in traces:
    if trace.startswith("4"):
        continue
    file_stream=open(trace,"rt")
    contents=file_stream.readlines()

    #trace name
    #print(trace[:trace.index(".",4)])

    #avg miss latency
    #print(contents[line_no])
    _temp=contents[line_no].split()
    #print(_temp[4])
    avg_miss_latency+=(float)(_temp[4])
    file_stream.close()

print("AVG = ",'%.2f'%(float)((float)(avg_miss_latency)/(float)(no_of_traces)))