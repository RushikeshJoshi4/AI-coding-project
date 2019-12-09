from matplotlib import pyplot as plt

for combination in ["BT","FC"]:
    mean_times = pkl.load(open("mean_times_"+combination, 'wb'))
    success_rates = pkl.load(open("success_rates_"+combination, 'wb'))
    x = mean_times.keys()
    y = mean_times.values()
    plt.plot(x, y)
    x = success_rates.keys()
    y = success_rates.values()
    plt.plot(x,y)
    plt.show()