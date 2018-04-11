import matplotlib.pyplot as plt
import numpy as np
import sys

def read_data(fn):
    data = []
    with open(fn,"r") as fl:
        for line in fl:
            data.append([float(i.strip()) for i in line.split(",")])
    return data

def main():
    data1 = read_data(sys.argv[1])[:90]  # Ridge
    data2 = read_data(sys.argv[2])[:90]  # Decision Tree
    #data3 = read_data(sys.argv[3])[:90]  # Random Forest

    #plot r2_score vs feature count
    x = [row[0] for row in data1]

    f1_1, f1_2 = [row[1] for row in data1],[row[1] for row in data2]#, [row[1] for row in data3]
    plt.xlabel('Feature Count')
    plt.ylabel('R2 Score')
    plt.title('Performance of Ridge and Decision Tree Models')
    plt.scatter(x,f1_1, s=10, color = 'green', label = "Ridge")
    plt.scatter(x,f1_2, s=10, color = 'blue', label = "Decision Tree")
    #plt.scatter(x,f1_3, s=10, color = 'red', label = "Random Forest")
    plt.legend()

    plt.show()

if __name__ == '__main__':
    main()
