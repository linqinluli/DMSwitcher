#%%
import csv
import os
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description="Process log file and write to CSV.")
parser.add_argument('file_path', type=str, help='Path to the log file')
args = parser.parse_args()

file_path = args.file_path
kernel_name = "4.11.0-fastswap"
backend = "rdma"
thp_state = "on"
cpu_num = 32

flag = 0
with open(file_path, encoding='utf-8') as file_obj:
    lines = file_obj.readlines()

data = []
with open("./test.csv", "a", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["kernel", "backend", "thp on/off", "cpu", "workload", "workload size", "page fault", "sys time", "user time", "wall time", "GFlops", "img/sec", "RSS"])

for i in range(len(lines)):
    pf = 0
    stime = 0
    utime = 0
    wtime = 0
    dataline = []
    is_data = 0
    imgsec = 0
    GFloops = 0
    if '0 memory limit to ' in lines[i]:
        model_name = str(lines[i].split()[1])
        model_name = model_name[:-1]
        local_ratio = float(str(lines[i].split()[5])[:-1])/100
    if 'Maximum resident set size (kbytes):' in lines[i]:
        maxrss = float(lines[i].split()[5])
    if lines[i] == 'Size   LDA    Align.  Average  Maximal\n':
        flag = 1
        linelist = lines[i+1].split()
        GFloops = float(linelist[4])
    if 'total images/sec' in lines[i]:
        flag = 2
        imgsec = float(lines[i].split()[2])
      
    if lines[i] == 'Major Page Faults,System Time,User Time,Wall Time\n':
        is_data = 1
        linelist = lines[i+1].split(",")
        pf = int(linelist[0])
        stime = float(linelist[1])
        utime = float(linelist[2])
        wtime = float(linelist[3])
    
    if is_data == 1:
        if flag == 1:
            imgsec = 0
        if flag == 2:
            GFloops = 0

        
        dataline = [kernel_name, backend, thp_state, cpu_num, model_name, local_ratio, pf, stime, utime, wtime, GFloops, imgsec, maxrss]
        with open("test.csv", "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(dataline)
        flag = 0
        print(pf, stime, utime, wtime, GFloops, imgsec, maxrss)
# %%
