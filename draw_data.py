import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
def draw_data(filename):
    try:
        with open(filename) as f:
            lists = f.readline().split(',')
        data = [float(x) for x in lists]
        print(data)
        plt.plot(data)
        plt.show()
    except FileNotFoundError:
        print(f"文件 {filename} 未找到。")
    except Exception as e:
        print(f"读取文件时发生错误：{e}")
draw_data(filename = "./data/1729403814.txt")

