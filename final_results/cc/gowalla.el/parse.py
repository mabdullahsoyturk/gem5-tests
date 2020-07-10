import glob
import os

dir_names = glob.glob("prefetch_*")
names = []
miss_rates = []

for dir_name in dir_names:
    os.chdir(dir_name)
    myCmd = os.popen('grep "l2.overall_miss_rate::total" stats.txt').readlines()
    line = myCmd[1].strip()

    temp = dir_name.split("_")
    name = "".join([temp[1], "_", temp[2]])
    names.append(name)

    miss_rate = line.split()[1]
    miss_rates.append(miss_rate)

    os.chdir("../")

names_csv = ','.join(names)
miss_rates_csv = ','.join(miss_rates)

with open("results.csv", "w") as results:
    results.write(names_csv + "\n")
    results.write(miss_rates_csv)