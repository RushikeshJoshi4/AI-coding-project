import pandas as pd
from statistics import mean, stdev
import operator
import pickle as pkl

def foo():
    columns = ["Mean(SD) Total time","Hardest M","Half-solvable M","Combination of methods"]
    df = pd.DataFrame(columns = columns)
    combinations = [
            # "BT", 
            # "FC", 
            # "FC MRV",
            # "FC MRV LCV",
            # "FC MAD LCV",
            "FC MAD LCV NOR"
        ]

    filename_base = "../../outputs/"+"exe_times_"
    
    for i, combination in enumerate(combinations):
        exe_times = {}
        outputs = {}
        mean_times = {}
        print(combination)
        filename = filename_base+ "_".join(combination.split())+".txt"
        file = open(filename, 'r')
        print(filename)
        for line in file.readlines():
            _, _, m, _, time, output = line.split()
            if m not in exe_times:
                exe_times[m] = []
            exe_times[m].append(float(time))
            if m not in outputs:
                outputs[m] = []
            outputs[m].append(bool(output))
        for m in exe_times.keys():
            mean_times[m] =  mean(exe_times[m])
        
        hardest_m = max(mean_times.items(), key = lambda x: x[1])[0]
        mean_of_hardest_m = mean_times[hardest_m]
        sd_of_hardest_m = stdev(exe_times[hardest_m])
        half_solvable_m = 0
        
        row = [ str(mean_of_hardest_m)+"("+str(sd_of_hardest_m)+")", 
                        hardest_m,
                        half_solvable_m,
                        "+".join(combination.split())
                ]
        # print(row)
        df.loc[i] = row
        # print(df.head())
        # df.to_csv("../outputs/stats_for_regular_sudoku.csv")

        if combination == "BT" or combination=="FC":
            pkl.dump(mean_times, open("mean_times_"+combination, 'wb+'))
            success_rates = {}

            for m in outputs.keys():
                successses = outputs[m].count(True)
                total = len(outputs[m])
                success_rates[m] = successses / total
            pkl.dump(success_rates, open("success_rates_"+combination, 'wb+'))
    print(df)
    df.to_csv("../../outputs/stats_for_regular_sudoku.csv")

foo()