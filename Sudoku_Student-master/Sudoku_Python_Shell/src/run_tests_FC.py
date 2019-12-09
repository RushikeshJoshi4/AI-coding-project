from __future__ import print_function
from Main import main
import os
import time
import sys

import time
from wrapt_timeout_decorator import *

@timeout(400)
def main_decorator(args):
    start_time = time.time()
    output = main(args)
    end_time = time.time()
    return [end_time - start_time,output]

def foo():
    p, q = (3, 4)
    no_of_tables = 4

    base = "../../boards_for_report/"
    out_file_dir = "../../outputs/"
    out_file_name = out_file_dir+"monster_exe_times_FC.txt"
    
    pathlib.Path(out_file_dir).mkdir(parents=True, exist_ok=True)
    if os.path.exists(out_file_name):
        os.remove(out_file_name)

    out_file = open(out_file_name, 'a')
    
    ms = list(range(0,20,5))+list(range(20, 30, 1))+list(range(30, 45, 5))
    print(ms)
    for m in ms:
        dir_name = "boards_p_"+str(p)+"_q_"+str(q)+"/m_"+str(m)+"/"

        filenames = os.listdir(base+dir_name)
        filenames = sorted(filenames)
        count = 0
        for filename in filenames:
            if count>=no_of_tables:
                break
            args = ["Main.py", ["FC"], base+dir_name+filename, False]
            try:
                exe_time, output = main_decorator(args)
                count += 1
            except TimeoutError as e:
                exe_time, output = [-1,-1]
                continue        
            print("{} {} {} {} {} {}".format(p, q, m, filename, exe_time, output), file=out_file)    
            print("{} {} {} {} {} {}".format(p, q, m, filename, exe_time, output)+" done!")
            # break
        # break
    # break

foo()
