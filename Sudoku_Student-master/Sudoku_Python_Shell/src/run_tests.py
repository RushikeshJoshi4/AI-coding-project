from __future__ import print_function
from Main import main
import os
import time
import sys

import time
from wrapt_timeout_decorator import *

@timeout(200)
def main_decorator(args):
    #print(args)
    start_time = time.time()
    output = main(args)
    end_time = time.time()
    return [end_time - start_time,output]

def enablePrint():
    sys.stdout = sys.__stdout__

def foo():
    combinations = [
        "", 
        "FC", 
        "FC MRV",
        "FC MRV LCV",
        "FC MAD LCV",
        "FC MAD LCV NOR"
    ]

    '''
    4
    4
    10
    20
    20
    20
    '''

    combinations = [combination.split() for combination in combinations]
    ps = [3]
    qs = [3]

    base = "../../boards_for_report/"
    out_file_dir = "../../outputs/"
    out_file_name = out_file_dir+"exe_times.txt"
    
    pathlib.Path(out_file_dir).mkdir(parents=True, exist_ok=True)
    if os.path.exists(out_file_name):
        os.remove(out_file_name)

    out_file = open(out_file_name, 'a')
    for p, q in zip(ps, qs):
        for m in reversed(range(0, 1)):
            dir_name = "boards_p_"+str(p)+"_q_"+str(q)+"/m_"+str(m)+"/"

            filenames = os.listdir(base+dir_name)
            filenames = sorted(filenames)
            # filename = 'board_11.txt'

            # start_time =time.time()
            # combination = combinations[0]
            # args = ["Main.py", combination, base+dir_name+filename, "False"]
            # try:
            #     exe_time = main_decorator(args)
            # except TimeoutError as e:
            #     exe_time = -1
            # print("{}: {}".format(base+dir_name+filename,exe_time), file=out_file)    
            # print(base+dir_name+filename+" done all combos!")

            for filename in filenames:
                for combination in combinations:
                    # start_time =time.time()
                    args = ["Main.py", combination, base+dir_name+filename, False]
                    try:
                        exe_time, output = main_decorator(args)
                    except TimeoutError as e:
                        exe_time, output = [-1,-1]
                    #enablePrint()

                    print("{}: {} {}".format(base+dir_name+filename,exe_time, output), file=out_file)    
                print(base+dir_name+filename+" done all combos!")
                # break
            # break
        # break

foo()
